from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, current_app, abort
from flask_login import current_user, login_required, logout_user

from app import db, avatars
from app.forms import EditProfileForm, EmptyForm, PostForm
from app.main import main
from app.model import User, Post, Role


@main.before_app_request
def before_request():
    Role.insert_roles()
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    # g.locale = str(get_locale())


# TODO: 简化重复代码
@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        body = Post(body=form.body.data, author=current_user)
        db.session.add(body)
        db.session.commit()
        flash('Your post is now live!', category="success")
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    for post in posts:
        post.body_html = Post.breviary(post.body_html)
    show_followed = False
    return render_template('index.html', title='Home', form=form,
                           show_followed=show_followed,
                           posts=posts, pagination=pagination)


@main.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    for post in posts:
        post.body_html = Post.breviary(post.body_html)
    return render_template('index.html', title='Explore',
                           posts=posts, pagination=pagination)


@main.route('/user/<username>')
@login_required
def user(username):
    c_user = User.query.filter_by(username=username).first_or_404()
    fans = c_user.followers.all()
    page = request.args.get('page', 1, type=int)
    pagination = c_user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    for post in posts:
        post.body_html = Post.breviary(post.body_html)
    form = EmptyForm()
    return render_template('main/user.html',
                           user=c_user, posts=posts,
                           pagination=pagination,
                           form=form, fans=fans)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        # head portrait
        current_user.avatar = avatars.save(form.avatar.data)
        db.session.commit()
        flash('Your changes have been saved.', category="info")
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', title='Edit Profile', form=form)


@main.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        f_user = User.query.filter_by(username=username).first()
        if f_user is None:
            flash('User %s not found.' % username, category="danger")
            return redirect(url_for('main.index'))
        if f_user == current_user:
            flash('You cannot follow yourself!', category="warning")
            return redirect(url_for('main.user', username=username))
        current_user.follow(f_user)
        db.session.commit()
        flash('You are following %s!' % username, category="success")
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@main.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        c_user = User.query.filter_by(username=username).first()
        if c_user is None:
            flash('User %s not found.' % username, category="danger")
            return redirect(url_for('main.index'))
        if c_user == current_user:
            flash('You cannot unfollow yourself!', category="warning")
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(c_user)
        db.session.commit()
        flash('You are not following %s.' % username, category="success")
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@main.route('/del_user')
@login_required
def del_user(id):
    if current_user.id != id:
        abort(403)
    db.session.delete(db.session.query(User).get(id))
    # TODO: delete fans relationship
    db.session.commit()
    logout_user()


@main.route('/remake')
def remake():
    return render_template('main/remake.html')
