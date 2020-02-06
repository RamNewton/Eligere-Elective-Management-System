#Importing modules used for creating Form objects
from flask_wtf import FlaskForm
import re

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
        
        if len(username.data) < 5 or len(username.data) > 16:
            raise ValidationError("Username should be between 5 to 16 characters long")

        pat = re.compile("^[\w\d]+$")
        if pat.match(username.data) is None:
            raise ValidationError('Username can contain only uppercase, lowercase characters or digits')
        

    def validate_password(self, password):
        pat1 = re.compile(".*[a-z].*")
        pat2 = re.compile(".*[A-Z].*")
        pat3 = re.compile(".*\d.*")
        # pat4 = re.compile(".*[+\-!@#$%\^&\*\.].*")
        passPat = re.compile("^[\w\d+\-!@#$%\^&\*\.]+$")
        if( len(password.data) < 8 or len(password.data) > 16 ):
            raise ValidationError("Password should be between 8 to 16 characters long")
        
        if(pat1.match(password.data) and pat2.match(password.data) and pat3.match(password.data) and passPat.match(password.data)):
            pass
        else:
            raise ValidationError("Password should contain atleast one lowercase, one uppercase and one digit")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_role(self, role):
        roles = ['Chairperson', 'Student', 'Faculty']
        if role.data not in roles:
            raise ValidationError("Please enter one of the following : Chairperson, Student or Faculty")