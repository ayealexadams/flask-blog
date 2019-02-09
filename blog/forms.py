from blog.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email address", validators=[DataRequired(), Email(), Length(min=2, max=120)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Register")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError("Username exists. Please choose another one.")

	def validate_email(self, email):
		email = email.data.lower()
		user = User.query.filter_by(email=email).first()

		if user:
			raise ValidationError("Email exists. Please use a different one.")


class LoginForm(FlaskForm):
	email = StringField("Email address", validators=[DataRequired(), Email(), Length(min=2, max=50)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
	remember = BooleanField("Remember me")
	submit = SubmitField("Login")
	

class UpdateAccountForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email address", validators=[DataRequired(), Email(), Length(min=2, max=120)])
	account_icon = FileField("Update account icon", validators=[FileAllowed(["jpg", "png"])])
	submit = SubmitField("Update")

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()

			if user:
				raise ValidationError("Username exists. Please choose another one.")

	def validate_email(self, email):
		if email.data != current_user.email:
			email = email.data.lower()
			user = User.query.filter_by(email=email).first()

			if user:
				raise ValidationError("Email exists. Please use a different one.")


class CreatePostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired(), Length(max=100)])
	content = TextAreaField("Content", validators=[DataRequired()])
	submit = SubmitField("Post")


class UpdatePostForm(CreatePostForm):
	pass


class RequestResetPasswordForm(FlaskForm):
	email = StringField("Email address", validators=[DataRequired(), Email(), Length(min=2, max=120)])
	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
		email = email.data.lower()
		user = User.query.filter_by(email=email).first()

		if user is None:
			raise ValidationError("Email does not exist. Please try again.")


class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Reset Password")
