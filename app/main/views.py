from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User, Post
from .. import db
from .forms import UpdateAccountForm
from flask_login import login_required, current_user
import datetime

# Views


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to Perfect Blog app'



    return render_template('index.html', title=title)




