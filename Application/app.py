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


if __name__ == '__main__':
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.jinja_env.auto_reload = True
	app.run(debug=True)