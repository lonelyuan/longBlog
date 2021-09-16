from flask import Blueprint

comments = Blueprint('comments', __name__)

from app.comments import routes