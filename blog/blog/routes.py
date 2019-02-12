from flask import Blueprint, render_template, request

from blog.models import Post

blog = Blueprint("blog", __name__)


@blog.route("/index")
@blog.route("/")
def index():
    page_num = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page_num)

    return render_template("index.html", posts=posts)


@blog.route("/about")
def about():
    return render_template("about.html", title="About")
