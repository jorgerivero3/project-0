from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from Application.models import User


class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("That username is taken. Please choose a different one.")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField('Login')

class newItem(FlaskForm):
	itemName = StringField("Name of listed item", validators=[DataRequired(), Length(min=2, max=20)])
	description = TextAreaField("Item description", validators=[DataRequired(), Length(max=750)])
	itemPrice = IntegerField("Price",validators=[DataRequired(), NumberRange(min=0, max=100000)])
	itemPic = FileField("Image of item", validators=[FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')])


