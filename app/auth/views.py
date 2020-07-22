from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required
from . import auth
from ..models import login_user
from .forms import LoginForm,RegistrationForm
from .. import db



@auth.route("/register",methods=['GET','POST'])
def register():
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



@auth.route("/login", method=['Get','Post'])
form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
