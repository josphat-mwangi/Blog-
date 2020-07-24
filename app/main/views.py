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


@main.route('/user/<uname')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)

