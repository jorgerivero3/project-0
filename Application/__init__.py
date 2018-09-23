from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_mail import Mail

PEOPLE_FOLDER = os.path.join('static', 'profile_pics')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c435bd07880364149cdf9661f1994db4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://N_A:kendrick8@project-0.c7ixro14gllf.us-east-2.rds.amazonaws.com/LaigsCrist'
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from Application import routes
