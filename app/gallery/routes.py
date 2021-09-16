import os

from flask import render_template, flash, current_app, redirect, url_for, abort, request
from flask_login import login_required, current_user

from app.gallery import gallery
from app.model import Image, Comment
from app import db, photos
from app.forms import ImageForm, CommentForm


@gallery.route('/', methods=['GET', 'POST'])
@gallery.route('/index', methods=['GET', 'POST'])
def index():
    offset = int(request.args.get('offset')) if request.args.get('offset') else 1
    image_sum = db.session.query(Image).count()
    images = db.session.query(Image)[0:4*offset]
    return render_template('gallery/index.html', title='Gallery',
                           path="/static/uploads",
                           offset=offset,
                           image_sum=image_sum,
                           images=images)


@gallery.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = ImageForm()
    if form.validate_on_submit():
        image = Image(author_id=current_user.id,
                      filename=photos.save(form.photo.data),
                      describe=form.describe.data)
        db.session.add(image)
        db.session.commit()
        flash('File uploaded.', category="success")
    return render_template('gallery/upload.html', title='Gallery', form=form)


@gallery.route('/<int:id>', methods=['GET', 'POST'])
def detail(id):
    image = Image.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, type="image",
                          image_id=image.id,
                          author_id=current_user._get_current_object().id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.', category="success")
        return redirect(url_for('.detail', id=image.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (image.comments.count() - 1) // \
               current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = image.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('gallery/detail.html', title='Photo Detail',
                           image=image,form=form,
                           path="/static/uploads",
                           comments=comments,
                           pagination=pagination)


@gallery.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    image = Image.query.get_or_404(id)
    if current_user.id != image.author_id:
        abort(403)
    file_path = photos.path(image.filename)
    os.remove(file_path)
    db.session.delete(image)
    db.session.commit()
    flash('The image has been deleted.', category="success")
    return redirect(url_for('gallery.index'))


@gallery.route('/loadmore/<int:offset>', methods=['GET', 'POST'])
def loadmore(offset):
    image_sum = db.session.query(Image).count()
    if offset*4 >= image_sum:
        flash('没有更多图片了，或许你可以上传？', category="warning")
        redirect(url_for('gallery.index', offset=offset))
    return redirect(url_for('gallery.index', offset=offset+1))
