from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, abort
from flask_login import current_user, login_required

from app import db
from app.forms import CommentForm
from app.model import Comment, User
from app.comments import comments


@comments.route('/reply/<int:id>', methods=['GET', 'POST'])
@login_required
def reply(id): # comment_id 当前评论
    comments_id_list = Comment.view_dialogue(id)
    print(comments_id_list)
    comments = [Comment.query.get_or_404(id) for id in comments_id_list]
    reply_id = request.args.get('replyid')
    post_id = request.args.get('postid')
    print(reply_id)
    reply_user = User.query.get(Comment.query.get_or_404(reply_id).author_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, type="comment",
                          reply_id=reply_id,
                          reply_name=reply_user.username,
                          post_id=post_id,
                          author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.', category="success")
        return redirect(url_for(".reply", id=comment.id)+"?replyid=%s&postid=%s" % (reply_id, post_id))
    return render_template('comments/reply.html', title="Reply",
                           form=form,
                           reply_user=reply_user,
                           comments=comments)


@comments.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    comment = Comment.query.get_or_404(id)
    post_id = request.args.get('postid')
    print(post_id, comment.author_id, comment.post_id)
    if current_user.id != comment.post_id and current_user.id != comment.author_id:
        abort(403)
    db.session.delete(db.session.query(Comment).get(id))
    db.session.commit()
    flash("delete complete")
    return redirect(request.referrer)
