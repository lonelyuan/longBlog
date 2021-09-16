from flask import redirect, url_for, request, abort
import flask_admin
from flask_admin import Admin, expose
from flask_admin.contrib import sqla
from flask_login import current_user
from app import db
from app.model import User, Post, Comment, Image


class MyAdminIndexView(flask_admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return super(MyAdminIndexView, self).index()


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_administrator()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


admin = Admin(name='microblog', index_view=MyAdminIndexView(),  template_mode='bootstrap4')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Comment, db.session))
admin.add_view(MyModelView(Image, db.session))
