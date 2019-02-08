import os
import secrets

from blog import app, db, bcrypt
from blog.models import User, Post
from blog.forms import RegisterForm, LoginForm, UpdateAccountForm, CreatePostForm, UpdatePostForm


from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image


def save_icon(account_icon):
	file_hex = secrets.token_hex(8)
	_, file_ext = os.path.splitext(account_icon.filename)
	file_name = file_hex + file_ext
	file_path = os.path.join(app.root_path, "static", "account_icons", file_name)
	
	output_size = (125, 125)
	final_icon = Image.open(account_icon)
	final_icon.thumbnail(output_size)
	final_icon.save(file_path)

	return file_name


@app.route("/index")
@app.route("/")
def index():
	page_num = request.args.get("page", 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page_num)

	return render_template("index.html", posts=posts)


@app.route("/about")
def about():
	return render_template("about.html", title="About")


@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	legend = "New Post"
	title = post.title
	return render_template("post.html", title=title, post=post, legend=legend)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)

	if post.author != current_user:
		abort(403)

	form = UpdatePostForm()

	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()

		flash(f"Your post has been updated!", "success")
		return redirect(url_for("post", post_id=post.id))

	elif request.method == "GET":
		form.title.data = post.title
		form.content.data = post.content
		
		legend = "Update Post"
		title = f"Update {post.title}"

	return render_template("create_update_post.html", title=title, form=form, legend=legend)


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)

	if post.author != current_user:
		abort(403)

	db.session.delete(post)
	db.session.commit()

	flash(f"Your post has been deleted!", "success")
	return redirect(url_for("index"))


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
	form = CreatePostForm()

	if form.validate_on_submit():
		author = current_user
		title = form.title.data
		content = form.content.data
		post = Post(author=author, title=title, content=content)

		db.session.add(post)
		db.session.commit()

		flash(f"Your post has been created!", "success")
		return redirect(url_for("index"))

	legend = "New Post"

	return render_template("create_update_post.html", title="Create Post", form=form, legend=legend)


@app.route("/user/<string:username>/posts")
def user_posts(username):
	user = User.query.filter_by(username=username).first_or_404()

	page_num = request.args.get("page", 1, type=int)
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=5, page=page_num)

	return render_template("user_posts.html", user=user, posts=posts)


@app.route("/account", methods=["GET", "POST"])
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
		return redirect(url_for("account"))

	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email

	account_icon = url_for('static', filename=f"account_icons/{current_user.account_icon}")
	
	return render_template("account.html", title="account", form=form, account_icon=account_icon)


@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegisterForm()

	if form.validate_on_submit():
		username = form.username.data
		email = form.email.data.lower()
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("UTF-8")

		new_user = User(username=username, email=email, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()

		flash(f"Your account has been created! You are now able to login.", "success")
		return redirect(url_for('login'))

	return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

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
				return redirect(url_for('index'))
		else:
			flash(f"Unsuccessful login! Please try again.", "danger")

	return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))
