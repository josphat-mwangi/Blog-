from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Required,Email,EqualTo
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    username = StringField("Enter Username",validators=[DataRequired(),length(min=2, max=2)])

    email = StringField("Enter Email address", validators=[DataRequired(),email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('submit = S')])