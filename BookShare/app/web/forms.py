from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from app.models import User

class BookForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(min=1, max=25)])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=25)])
    description = TextAreaField('Descripition', validators=[DataRequired(), Length(min=1, max=1000)])

    algorithms = BooleanField('algorithms')
    programming = BooleanField('programming')
    math = BooleanField('math')
    software = BooleanField('software')
    other = BooleanField('other')

    submit = SubmitField('submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username',  validators=[DataRequired(), Length(min=4, max=25)])

    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        Length(min=4, max=25)
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, field): #检查用户名是否已存在
        username = field.data
        count = User.query.filter_by(username=username).count()
        if count != 0:
            raise ValidationError("username is already taken")


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4, max=25)])
    submit = SubmitField('Login')

    def validate_username(self, field):
        username = field.data
        count = User.query.filter_by(username=username).count()
        if count == 0:
            raise ValidationError("account doesn't exist")

