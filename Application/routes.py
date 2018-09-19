from flask import render_template, url_for, flash, redirect, request
from Application import app
from Application.forms import RegistrationForm, LoginForm
from Application.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
	return render_template('./index.html', name='App Title')


@app.route("/register", methods=['GET', "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
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


@app.route("/newItem")
def itemListing():
	form = newItem()
	return render_template("newItem.html", title="New Item Listing", form=form)


@app.route("/home")
@app.route("/ads")
def home():
	return render_template("ads.html", title="SALES WOW")


@app.route("/logout")
def loutout():
	logout_user()
	return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
	return render_template('account.html', title="Account")
