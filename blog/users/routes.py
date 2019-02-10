from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetPasswordForm, ResetPasswordForm
from blog.users.utils import save_icon, send_reset_password_email


users = Blueprint("users", __name__)


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
	form = UpdateAccountForm()

	if form.validate_on_submit():
		if form.account_icon.data:
			account_icon = save_icon(form.account_icon.data)
			current_user.account_icon = account_icon

		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()

		flash(f"Your account has been updated!", "success")
		return redirect(url_for("users.account"))

	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email

	account_icon = url_for('static', filename=f"account_icons/{current_user.account_icon}")
	
	return render_template("account.html", title="account", form=form, account_icon=account_icon)


@users.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('blog.index'))

	form = RegisterForm()

	if form.validate_on_submit():
		username = form.username.data
		email = form.email.data.lower()
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("UTF-8")

		new_user = User(username=username, email=email, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()

		flash(f"Your account has been created! You are now able to login.", "success")
		return redirect(url_for('users.login'))

	return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('blog.index'))

	form = LoginForm()

	if form.validate_on_submit():
		email = form.email.data.lower()
		user = User.query.filter_by(email=email).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash(f"Successful log in!", "success")
			
			next_page = request.args.get("next")
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('blog.index'))
		else:
			flash(f"Unsuccessful login! Please try again.", "danger")

	return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('blog.index'))


@users.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('blog.index'))

	form = RequestResetPasswordForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_password_email(user)
		flash(f"An email has been sent to {form.email.data}. Follow the instructions to reset your password.", "info")
		return redirect(url_for("users.login"))

	return render_template("reset_password_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('blog.index'))

	user = User.verify_reset_token(token)

	if user is None:
		flash("That token has expired or is invaild.", "warning")
		return redirect(url_for("users.reset_password_request"))

	form = ResetPasswordForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("UTF-8")

		user.password = hashed_password
		db.session.commit()

		flash(f"Your password has been reset! You are now able to login.", "success")
		return redirect(url_for('users.login'))

	return render_template("reset_password.html", title="Reset Password", form=form)
