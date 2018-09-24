from flask import render_template, url_for, flash, redirect, request, abort
from Application import application, db, bcrypt, mail
from Application.forms import (RegistrationForm, LoginForm, UpdateInfo, newItem, 
								RequestResetForm, ResetPasswordForm)
from Application.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from flask_mail import Message

#what do these lines do?
#def before_request():
#	app.jinja_env.cache = {}
#
#app.before_request(before_request)

@application.route('/', methods=['GET'])
def index():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	full_filename = os.path.join(application.config["UPLOAD_FOLDER"], 'default.png')
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
	return render_template("/index.html", title="App Title", posts=posts, user_image = full_filename)


@application.route("/register", methods=['GET', "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	print("Register form")
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account created! You can now log in', 'success')
		return redirect(url_for('login'))
	return render_template("register.html", title="Register", form=form)


@application.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("Login Unsuccessful. Email and/or password Incorrect", "danger")
	return render_template('login.html', title="Login", form=form)


@application.route("/listings/new", methods=['GET', 'POST'])
@login_required
def itemListing():
	form = newItem()
	if form.validate_on_submit():
		_, f_ext = os.path.splitext(form.itemPic.data.filename)
		post = Post(itemName=form.itemName.data, description=form.description.data, itemPrice=form.itemPrice.data, user=current_user.id, ext=f_ext)
		db.session.add(post)
		db.session.commit()
		save_pic(form.itemPic.data, str(post.id), f_ext)
		flash('Item Listed!', 'success')
		return redirect(url_for('home'))
	return render_template("newItem.html", title="New Item Listing", form=form, legend='New Listing')

def save_pic(form_picture, post_id, extension):
	picture_fn = post_id + extension
	picture_path = os.path.join(application.root_path, 'static/listing_pics', picture_fn)
	output_size = (500,500)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@application.route("/home")
@application.route("/ads")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template("ads.html", title="Ads Listings", posts=posts)


@application.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))


@application.route("/account")
@login_required
def account():
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title="Account", image_file=image_file)

@application.route("/updateInfo", methods=['GET', 'POST'])
@login_required
def updateInfo():
	form = UpdateInfo()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Info Updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('updateInfo.html', title="Update your Information", image_file=image_file, form=form)


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(application.root_path, 'static/profile_pics', picture_fn)
	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@application.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.itemName, post=post)


@application.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = newItem()
	if form.validate_on_submit():
		post.itemName = form.itemName.data
		post.description = form.description.data
		post.itemPrice = form.itemPrice.data
		post.itemPic = form.itemPic.data
		db.session.commit()
		flash('Post Updated', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.itemName.data = post.itemName
		form.description.data = post.description
		form.itemPrice.data = post.itemPrice
		form.itemPic.data = post.itemPic
	return render_template('listing.html', title='Update your Post', form=form, legend='Update Post')


@application.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if (current_user.admin != True) and (post.author != current_user):
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Post Deleted', 'success')
	return redirect(url_for('home'))


@application.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	image_file = url_for('static', filename='profile_pics/' + user.image_file)
	posts = Post.query.filter_by(author=user)\
	.order_by(Post.date_posted.desc())\
	.paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user, image_file=image_file)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@utexas.edu', recipients=[user.email])
	msg.body = f''' To reset your password, click the following link, or copy and
paste it into your web browser:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then please ignore this email.
	'''

@application.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@application.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('The reset token you are using is invalid or expired.')
		return redirect(url_for('password_retrieval'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Password has been updated.', 'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)