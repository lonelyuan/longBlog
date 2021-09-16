from flask import Blueprint

error = Blueprint('errors', __name__)

from app.errors import handlers

