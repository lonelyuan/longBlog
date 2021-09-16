from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, abort
from flask_login import current_user, login_required

from app import db
from app.forms import CommentForm, PostForm
from app.model import Post, Comment
from app.posts import posts


@posts.route('/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.', category="success")
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('posts/post.html', title="Post", posts=[post], form=form,
                           comments=comments, pagination=pagination)


@posts.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.', category="success")
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('posts/edit_post.html', form=form, id=post.id)


@posts.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    # TODO: delete associative comments
    db.session.commit()
    flash('The post has been deleted.', category="success")
    return redirect(url_for('main.index'))