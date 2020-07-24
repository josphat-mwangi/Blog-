from app import create_app
from flask import Blueprint
auth = Blueprint('auth',__name__)




from . import views,forms
