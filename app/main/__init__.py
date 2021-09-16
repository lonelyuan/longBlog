from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates/errors')

from app.main import routes, yxh
from app.model import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

"""
main:
- /, /index
    - PostForm
- /explore
- /edit_profile
"""
