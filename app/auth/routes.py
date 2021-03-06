from flask import render_template, flash, redirect, url_for, session
#This module handles login functionalities
from flask_login import login_user, logout_user, current_user, login_required

from app.auth.forms import *
from app import db
from app.auth import bp
from app.models import User, Faculty, Student, FacultyDetails, StudentDetails
from app.auth.email import send_password_reset_email

import jwt
from functools import wraps

def requires_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('role'):
                return redirect(url_for('main.index'))
            elif session.get('role') != role:
                flash("Access denied")
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#Login Endpoint
@bp.route('/login', methods=['GET', 'POST'])
def login():
    print("GET")
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        print("POST")
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        #Using session object to store the role of the User
        session['role'] = user.role
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)

#Logout Endpoint
@bp.route('/logout')
def logout():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    logout_user()
    #Removing the 'role' of the user from the session object on logout.
    if 'role' in session:
        if(session['role']):
            session.pop('role')
    return redirect(url_for('auth.login'))

#Should be scraped Later
#Helper function for register
def add_supporting_data(user, name):
    if(user.role == 'Faculty'):
        fac = Faculty(user_id = user.id, name = name, elective_id = "None")
        db.session.add(fac)
        db.session.commit()
        print(fac)

@bp.route('/registerFaculty', methods=['GET', 'POST'])
@requires_role('Chairperson')
def registerFaculty():
    form = RegistrationFaculty()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role = "Faculty")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        add_to_Faculty(user, form.fac_id.data)
        flash('New Faculty User successfully registered!')
        return redirect(url_for('main.index'))
    return render_template('auth/registerFaculty.html', title='Register Faculty', form=form)

def add_to_Faculty(user, fac_id):
    fac = Faculty(user_id = user.id, fac_id = fac_id, elective_id = "None")
    db.session.add(fac)
    db.session.commit()
    print(fac)

@bp.route('/registerStudent', methods=['GET', 'POST'])
@requires_role('Chairperson')
def registerStudent():
    form = RegistrationStudent()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role = "Student")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        add_to_Student(user, form.roll_number.data)
        flash('New Student User successfully registered!')
        return redirect(url_for('main.index'))
    return render_template('auth/registerStudent.html', title='Register Student', form=form)

def add_to_Student(user, roll_number):
    s = Student(user_id = user.id, roll_number = roll_number, elective_id1 = "None", elective_id2 = "None", elective_id3 = "None")
    db.session.add(s)
    db.session.commit()
    print(s)


#Admin Helper Functions
@bp.route('/addStudentDetails', methods=['GET', 'POST'])
@requires_role('Admin')
def addStudentDetails():
    form = AddStudentDetails()
    if form.validate_on_submit():
        roll_number = form.roll_no.data
        name = form.name.data
        department = form.department.data
        section = form.section.data
        batch = form.batch.data
        s = StudentDetails(roll_no = roll_number, name = name, department = department, section = section, batch = batch)
        db.session.add(s)
        db.session.commit()
        flash("Student Details Added")
        return redirect(url_for('auth.addStudentDetails'))
    return render_template('auth/admin/addStudentDetails.html', form = form)

#Admin Helper Functions
@bp.route('/addFacultyDetails', methods=['GET', 'POST'])
@requires_role('Admin')
def addFacultyDetails():
    form = AddFacultyDetails()
    if form.validate_on_submit():
        fac_id = form.fac_id.data
        name = form.name.data
        designation = form.designation.data
        department = form.department.data
        f = FacultyDetails(fac_id=fac_id, name=name, designation=designation, department=department)
        db.session.add(f)
        db.session.commit()
        flash("Faculty Details Added")
        return redirect(url_for('auth.addFacultyDetails'))
    return render_template('auth/admin/addFacultyDetails.html', form = form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)