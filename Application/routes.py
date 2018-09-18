from flask import render_template, url_for, flash, redirect
from Application import app
from Application.forms import RegistrationForm, LoginForm
from Application.models import User, Post


@app.route('/')
def index():
	return render_template('./index.html', name='App Title')


@app.route("/register", methods=['GET', "POST"])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f"Account created for {form.username.data}!", "success")
		return redirect(url_for('home'))
	return render_template('login.html', title="Login", form=form)


@app.route("/password_retrieval")
def passretrieval(): #need a form
	return render_template("password_retrieval.html", title="Get your password back")

@app.route("/newItem")
def itemListing():
	form = newItem()
	return render_template("newItem.html", title="New Item Listing", form=form)

@app.route("/home")
def home():
	return render_template("ads.html", title="SALES WOW")