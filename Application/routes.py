from flask import render_template, url_for, flash, redirect, request, abort
from Application import app, db, bcrypt
from Application.forms import RegistrationForm, LoginForm, UpdateInfo, newItem
from Application.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

#what do these lines do?
#def before_request():
#	app.jinja_env.cache = {}
#
#app.before_request(before_request)

@app.route('/')
def index():
	return render_template('./index.html', name='App Title')


@app.route("/register", methods=['GET', "POST"])
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


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(uesr, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("Login Unsuccessful. Email and/or password Incorrect", "danger")
	return render_template('login.html', title="Login", form=form)


@app.route("/password_retrieval")
def passretrieval(): #need a form
	return render_template("password_retrieval.html", title="Get your password back")


@app.route("/listings/new", methods=['GET', 'POST'])
# @login_required  <-- just for now -->
def itemListing():
	form = newItem()
	if form.validate_on_submit():
		post = Post(itemName=form.itemName.data, description=form.description.data, itemPrice=form.itemPrice.data, itemPic = form.itemPic, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Item Listed!', 'success')
		return redirect(url_for('home'))
	return render_template("newItem.html", title="New Item Listing", form=form, legend='New Listing')


@app.route("/home")
@app.route("/ads")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.dsc()).paginate(page=page, per_page=10)
	return render_template("ads.html", title="SALES WOW", posts=posts)


@app.route("/logout")
def loutout():
	logout_user()
	return redirect(url_for("home"))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
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
	return render_template('account.html', title="Account", image_file=image_file, form=form)

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'statis/profile_pics', picture_fn)
	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('listing.html', title=post.itemName, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
	return render_template('listing.html', title='update_post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Post Deleted', 'success')
	return redirect(url_for('home'))
	
