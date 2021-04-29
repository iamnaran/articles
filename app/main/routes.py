from flask import Blueprint, request, render_template

from app.models.Post import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.date_poasted.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/admin")
def admin():
    return render_template('admin/admin.html', title='Admin')
