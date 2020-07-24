from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required,DataRequired,length,Email,EqualTo,email_validator
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')
