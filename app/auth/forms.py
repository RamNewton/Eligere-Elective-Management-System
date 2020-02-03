#Importing modules used for creating Form objects
from flask_wtf import FlaskForm

#Importing classes for various fileds in forms
from wtforms import StringField, PasswordField, BooleanField, SubmitField

#Importing validators
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Required

#Importing table models from DataBase
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role', validators = [DataRequired()])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_role(self, role):
        roles = ['Chairperson', 'Student', 'Faculty']
        if role.data not in roles:
            raise ValidationError("Please enter one of the following : Chairperson, Student or Faculty")