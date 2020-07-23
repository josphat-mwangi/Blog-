from app import create_app
from flask import Blueprint
auth = Blueprint('auth',__name__)


app = create_app('development')
app.app_context().push()

from . import views,forms
