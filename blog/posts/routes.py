from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from blog import db
from blog.models import Post, User
from blog.posts.forms import PostForm

posts = Blueprint("posts", __name__)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    legend = "New Post"
    title = post.title
    return render_template("post.html", title=title, post=post, legend=legend)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash(f"Your post has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

        legend = "Update Post"
        title = f"Update {post.title}"

    return render_template("create_update_post.html", title=title, form=form, legend=legend)


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash(f"Your post has been deleted!", "success")
    return redirect(url_for("blog.index"))


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        author = current_user
        title = form.title.data
        content = form.content.data
        post = Post(author=author, title=title, content=content)

        db.session.add(post)
        db.session.commit()

        flash(f"Your post has been created!", "success")
        return redirect(url_for("blog.index"))

    legend = "New Post"

    return render_template("create_update_post.html", title="Create Post", form=form, legend=legend)


@posts.route("/user/<string:username>/posts")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()

    page_num = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(per_page=5, page=page_num)
    )

    return render_template("user_posts.html", user=user, posts=posts)
