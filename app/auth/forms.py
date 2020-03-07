#Importing modules used for creating Form objects
from flask_wtf import FlaskForm
import re

#Importing classes for various fileds in forms
from wtforms import StringField, PasswordField, BooleanField, SubmitField

#Importing validators
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Required

#Importing table models from DataBase
from app.models import User, Faculty, Student, FacultyDetails, StudentDetails

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

#To be Scrapped
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

class RegistrationFaculty(FlaskForm):
    fac_id = StringField('Faculty ID', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
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

    def validate_fac_id(self, fac_id):
        print("Faculty ID entered in form:", fac_id.data)
        f = FacultyDetails.query.filter_by(fac_id = fac_id.data).first()
        if f is None:
            raise ValidationError("Faculty ID not found in Database!")
        
        f = Faculty.query.filter_by(fac_id = fac_id.data).first()
        if f is not None:
            raise ValidationError("A user with this Faculty ID already exists")
        

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

class RegistrationStudent(FlaskForm):
    roll_number = StringField('Roll Number', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')
        
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
            raise ValidationError('Please use a different email address')

    def validate_roll_number(self, roll_number):
        s = StudentDetails.query.filter_by(roll_no = roll_number.data).first()
        if s is None:
            raise ValidationError("Roll Number not found in Database!")

        s = Student.query.filter_by(roll_number = roll_number.data).first()
        if s is not None:
            raise ValidationError("A user with this Roll Number already exists!")
    
class AddFacultyDetails(FlaskForm):
    fac_id = StringField('Faculty ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Add Faculty')

    def validate_faculty_id(self, fac_id):
        f = FacultyDetails.query.filter_by(fac_id = fac_id.data).first()
        if f is not None:
            raise ValidationError("Faculty ID already exists")

class AddStudentDetails(FlaskForm):
    roll_no = StringField('Roll No.', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    batch = StringField('Batch', validators=[DataRequired()])
    submit = SubmitField('Add Student')

    def validate_roll_no(self, roll_no):
        s = StudentDetails.query.filter_by(roll_no = roll_no.data).first()
        if s is not None:
            raise ValidationError("Roll Number already exists")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')