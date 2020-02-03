from flask import render_template, flash, redirect, url_for, session

#Importing the Forms Required
from app.main.forms import AddElectives
from flask_login import current_user, login_required

#Importing the database object used by the app
from app import db

#Importing table models using which data is added, removed, updated in the database
from app.models import InitialElectiveList, User, Faculty

from app.main import bp

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

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', role = session['role'])

#Chaiperson Role: Adding Electives to the InitialElectiveList Endpoint
@bp.route('/AddElectives', methods=['GET', 'POST'])
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
@bp.route('/ShowElectives')
@requires_role('Chairperson')
def showElectives():
    electives = InitialElectiveList.query.all()
    # print("These are the electives: \n", electives)
    return render_template('ShowElectives.html', title='Show Electives', electives = electives )

#Chairperson Role: GET method endpoint that removes an elective with given elective_id
@bp.route('/RemoveElective/<elective_id>')
@requires_role('Chairperson')
def funcRemoveElective(elective_id):
    tmp = InitialElectiveList.query.filter_by(electiveID=elective_id).first()
    if tmp is None:
        flash("Invalid Elective ID, cannot be removed")
        return(redirect(url_for('main.index')))
    else:
        obj = InitialElectiveList.query.filter_by(electiveID=elective_id).one()
        db.session.delete(obj)
        db.session.commit()
        return(redirect(url_for('main.showElectives')))

@bp.route('/ChooseElectiveToOffer')
@requires_role('Faculty')
def chooseElectiveToOffer():
    electives = InitialElectiveList.query.all()
    tmp = Faculty.query.filter_by(user_id = current_user.id).first()
    chosen_elective_id = tmp.elective_id
    return render_template('ChooseElectiveToOffer.html', title='Choose Elective to Offer', electives = electives, choice = chosen_elective_id)

#Faculty Role: GET method endpoint that updates the Faculty's choice in the Databse.
#A "None" entry indicates faculty hasn't chosen a course yet
@bp.route('/funcChooseElectiveToOffer/<elective_id>')
@requires_role('Faculty')
def funcChooseElectiveToOffer(elective_id):
    tmp = InitialElectiveList.query.filter_by(electiveID=elective_id).first()
    if (tmp is None) and elective_id != 'None':
        flash("Invalid Elective ID, cannot be removed")
        return(redirect(url_for('main.index')))
    else:
        tmp = Faculty.query.filter_by(user_id=int(current_user.id)).first()
        tmp.elective_id = str(elective_id)
        db.session.commit()
        print("User has chosen ", elective_id)
        return(redirect(url_for('main.chooseElectiveToOffer')))

#Faculty Role: Endpoint that shows the Elective Choice of all the faculty in the system so far
@bp.route('/ViewFacultyChoice')
@requires_role('Faculty')
def viewFacultyChoice():
    fac_list = Faculty.query.all()
    return render_template('ViewFacultyChoice.html', title='Electives Chosen by Faculty', fac_list = fac_list)