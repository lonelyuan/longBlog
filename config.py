import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 6
    COMMENTS_PER_PAGE = 3
    UPLOADED_AVATARS_DEST = 'app\\static\\avatars'
    UPLOADED_PHOTOS_DEST = 'app\\static\\uploads'
    UPLOADS_AUTOSERVE = True
    ADMIN_EMAIL = "1139369370@qq.com"
