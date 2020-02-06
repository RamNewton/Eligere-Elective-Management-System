from flask import render_template, flash, redirect, url_for, session
#This module handles login functionalities
from flask_login import login_user, logout_user, current_user, login_required

from app.auth.forms import LoginForm, RegistrationForm
from app import db
from app.auth import bp
from app.models import User, Faculty

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
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
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

#Endpoint to register new Users to the system
#(Currently accessible by anyone. Later we'll restrict it to Chairperson Role Only)
@bp.route('/register', methods=['GET', 'POST'])
@requires_role('Chairperson')
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role = form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        add_supporting_data(user, form.name.data)
        flash('New User successfully registered!')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', title='Register', form=form)

#Helper function for register
def add_supporting_data(user, name):
    if(user.role == 'Faculty'):
        fac = Faculty(user_id = user.id, name = name, elective_id = "None")
        db.session.add(fac)
        db.session.commit()
        print(fac)