import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, UploadSet, IMAGES
from sqlalchemy import MetaData

from config import Config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
moment = Moment()
pagedown = PageDown()  # I'll fuxk it
avatars = UploadSet('avatars', IMAGES)
photos = UploadSet('photos', IMAGES)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # file service
    configure_uploads(app, [avatars, photos])
    # plugin service
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    # blueprint service
    from app.admin import admin
    admin.init_app(app)
    from app.main import main as main_bp
    app.register_blueprint(main_bp)
    from app.errors import error as errors_bp
    app.register_blueprint(errors_bp)
    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.gallery import gallery as gallery_bp
    app.register_blueprint(gallery_bp, url_prefix='/gal')
    from app.posts import posts as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/post')
    from app.comments import comments as comments_bp
    app.register_blueprint(comments_bp, url_prefix='/comment')
    # logger service
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


