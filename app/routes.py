from flask import render_template, flash, redirect, url_for, session
from app import app

#Importing the Forms Required
from app.forms import LoginForm, AddElectives, RegistrationForm

#Importing the database object used by the app
from app import db

#Importing table models using which data is added, removed, updated in the database
from app.models import InitialElectiveList, User, Faculty

#This module handles login functionalities
from flask_login import login_user, logout_user, current_user, login_required

from functools import wraps

#Function that restricts access to certain webpages based on the type of user currently logged in.
#Eg. Faculty user cannot access "AddElectives" page. It can only be accessed by Chairperson user.

def requires_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('role'):
                return redirect(url_for('index'))
            elif session.get('role') != role:
                flash("Access denied")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#Note Each function in this file correspond to an endpoint in the WebApp
#Endpoints that can only be accessed when you are logged in has the "@login_required" decorator
#This is kind of the heart of the WebApp


#Dashboard Endpoint
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', role = session['role'])

#Login Endpoint
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        #Using session object to store the role of the User
        session['role'] = user.role
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

#Logout Endpoint
@app.route('/logout')
def logout():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    logout_user()
    #Removing the 'role' of the user from the session object on logout.
    if 'role' in session:
        if(session['role']):
            session.pop('role')
    return redirect(url_for('login'))

#Chaiperson Role: Adding Electives to the InitialElectiveList Endpoint
@app.route('/AddElectives', methods=['GET', 'POST'])
@login_required
@requires_role('Chairperson')
def addElectives():
    form = AddElectives()
    if form.validate_on_submit():
        elective = InitialElectiveList(electiveID = form.elective_id.data, electiveName = form.elective_name.data, electiveDescription = form.elective_description.data)
        db.session.add(elective)
        db.session.commit()
        flash("Added Elective!")
    return render_template('AddElectives.html',  title='Add Electives', form=form)

#Chairperson Role: Showing Electives that have been added so far Endpoint
@app.route('/ShowElectives')
@requires_role('Chairperson')
def showElectives():
    electives = InitialElectiveList.query.all()
    # print("These are the electives: \n", electives)
    return render_template('ShowElectives.html', title='Show Electives', electives = electives )

#Chairperson Role: GET method endpoint that removes an elective with given elective_id
@app.route('/RemoveElective/<elective_id>')
@requires_role('Chairperson')
def funcRemoveElective(elective_id):
    tmp = InitialElectiveList.query.filter_by(electiveID=elective_id).first()
    if tmp is None:
        flash("Invalid Elective ID, cannot be removed")
        return(redirect(url_for('index')))
    else:
        obj = InitialElectiveList.query.filter_by(electiveID=elective_id).one()
        db.session.delete(obj)
        db.session.commit()
        return(redirect(url_for('showElectives')))


#Faculty Role: Endpoint that let's the faculty choose what Elective they would like to offer
@app.route('/ChooseElectiveToOffer')
@requires_role('Faculty')
def chooseElectiveToOffer():
    electives = InitialElectiveList.query.all()
    tmp = Faculty.query.filter_by(user_id = current_user.id).first()
    chosen_elective_id = tmp.elective_id
    return render_template('ChooseElectiveToOffer.html', title='Choose Elective to Offer', electives = electives, choice = chosen_elective_id)


#Faculty Role: GET method endpoint that updates the Faculty's choice in the Databse.
#A "None" entry indicates faculty hasn't chosen a course yet
@app.route('/funcChooseElectiveToOffer/<elective_id>')
@requires_role('Faculty')
def funcChooseElectiveToOffer(elective_id):
    tmp = InitialElectiveList.query.filter_by(electiveID=elective_id).first()
    if (tmp is None) and elective_id != 'None':
        flash("Invalid Elective ID, cannot be removed")
        return(redirect(url_for('index')))
    else:
        tmp = Faculty.query.filter_by(user_id=int(current_user.id)).first()
        tmp.elective_id = str(elective_id)
        db.session.commit()
        print("User has chosen ", elective_id)
        return(redirect(url_for('chooseElectiveToOffer')))

#Faculty Role: Endpoint that shows the Elective Choice of all the faculty in the system so far
@app.route('/ViewFacultyChoice')
@requires_role('Faculty')
def viewFacultyChoice():
    fac_list = Faculty.query.all()
    return render_template('ViewFacultyChoice.html', title='Electives Chosen by Faculty', fac_list = fac_list)

#Endpoint to register new Users to the system
#(Currently accessible by anyone. Later we'll restrict it to Chairperson Role Only)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role = form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        add_supporting_data(user, form.name.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#Helper function for register
def add_supporting_data(user, name):
    if(user.role == 'Faculty'):
        fac = Faculty(user_id = user.id, name = name, elective_id = "None")
        db.session.add(fac)
        db.session.commit()
        print(fac)