from firebase import firebase
from forms import RegistrationForm, LoginForm
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import LoginManager

firebase = firebase.FirebaseApplication('https://project-0-1a188.firebaseio.com', authentication=None)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c435bd07880364149cdf9661f1994db4'
login_manager = LoginManager(app)


@app.route('/')
def index():
	return render_template('./index.html', name='App Title')


@app.route("/register", methods=['GET', "POST"])
def register():
	form = RegistrationForm()
	if request.method == "POST":
		user = firebase.post('/Users', form.username.data, form.email.data, form.password.data)
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

@app.route("/ads")
def ads():
	return render_template("ads.html", title="SALES WOW")

if __name__ == '__main__':
	app.run(debug=True)