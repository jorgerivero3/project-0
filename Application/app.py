# CONSIDER REDOING THIS FILE AS NAME CONFLICTS WITH VARIABLE AND
# WE ARE ALSO RESTRUCTURING TO USE AS A PACKAGE

from forms import RegistrationForm, LoginForm, newItem
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c435bd07880364149cdf9661f1994db4'
login_manager = LoginManager(app)

# this is just clearing the template cache so html/css changes actually render
def before_request():
	app.jinja_env.cache = {}

app.before_request(before_request)

@app.route('/')
def index():
	return render_template('./index.html', name='App Title')


@app.route("/register", methods=['GET', "POST"])
def register():
	form = RegistrationForm()
	if request.method == "POST":
		print(user)
		return redirect(index)
	return render_template("register.html", title="Register", form=form)


@app.route("/login")
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f"Account created for {form.username.data}!", "success")
		return redirect(url_for('index'))
	return render_template('login.html', title="Login", form=form)


@app.route("/password_retrieval")
def passretrieval(): #need a form
	return render_template("password_retrieval.html", title="Get your password back")

@app.route("/newItem")
def itemListing():
	form = newItem()
	return render_template("newItem.html", title="New Item Listing", form=form)

@app.route("/ads")
def ads():
	return render_template("ads.html", title="SALES WOW")

if __name__ == '__main__':
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.jinja_env.auto_reload = True
	app.run(debug=True)