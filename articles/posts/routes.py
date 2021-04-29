from flask import Blueprint, render_template, flash, redirect, request, abort, url_for
from flask_login import current_user, login_required
from articles import db
from articles.models.Post import Post
from articles.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@login_required
@posts.route("/posts/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your posts has been create!", 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='Create Post', form=form, legend="New Post")


@posts.route("/posts/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', title=post.title, post=post)


@login_required
@posts.route("/posts/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your posts has been update", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',form=form, legend="Update Post")


@login_required
@posts.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your posts has been deleted", 'success')
    return redirect(url_for('main.home'))
