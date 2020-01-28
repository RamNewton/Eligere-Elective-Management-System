from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Required
from wtforms.widgets import TextArea
from app.models import InitialElectiveList, User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddElectives(FlaskForm):
    elective_id = StringField("Elective ID", validators = [DataRequired()])
    elective_name = StringField("Elective Name", validators = [DataRequired()])
    elective_description = StringField("Elective Description", widget = TextArea(), validators = [DataRequired()])
    submit = SubmitField('Submit Elective')

    def validate_elective_id(self, elective_id):
        tmp = InitialElectiveList.query.filter_by(electiveID=elective_id.data).first()
        if tmp is not None:
            raise ValidationError('Please enter a different elective id.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators = [DataRequired()])
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