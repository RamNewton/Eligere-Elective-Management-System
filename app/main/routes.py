from flask import render_template, flash, redirect, url_for, session

#Importing the Forms Required
from app.main.forms import AddElectives
from flask_login import current_user, login_required

#Importing the database object used by the app
from app import db

#Importing table models using which data is added, removed, updated in the database
from app.models import *

from app.main import bp
from functools import wraps
import os
import json

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
    print(session['role'])
    if(session['role'] == 'Chairperson'):
        data = read_json()
        return render_template('index.html', title='Home', role = session['role'], data = data)

    elif(session['role'] == 'Faculty'):
        tmp = Faculty.query.filter_by(user_id = current_user.id).first()
        fac_id = tmp.fac_id
        elective_id = tmp.elective_id
        tmp = FacultyDetails.query.filter_by(fac_id = fac_id).first()
        data = {'name' : tmp.name, 'designation': tmp.designation, 'department' : tmp.department, 'id' : fac_id, 'elective_id': elective_id}
        return render_template('index.html', title='Home', role = session['role'], data = data)

    elif(session['role'] == 'Student'):
        tmp1 = Student.query.filter_by(user_id = current_user.id).first()
        allot = tmp1.allotted_elective
        rand = tmp1.random_elective
        roll_number = tmp1.roll_number
        tmp = StudentDetails.query.filter_by(roll_no = roll_number).first()
        data = {'name' : tmp.name, 'batch' : tmp.batch, 'department': tmp.department, 'section' : tmp.section, 'roll_number': roll_number, 'rand' : rand, 'allot' : allot}
        json = read_json()
        return render_template('index.html', title='Home', role = session['role'], data = data, json = json)

    else:
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
        return redirect(url_for('main.addElectives'))
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
    data = read_json()
    print(data["FacultyOpen"])
    if((data["FacultyOpen"]) == "False"):
        flash("You can no longer Change your Preference. The portal has been closed by the Chairperson")
        return(redirect(url_for('main.index')))

    electives = InitialElectiveList.query.all()
    tmp = Faculty.query.filter_by(user_id = current_user.id).first()
    # print(tmp)
    # print(Faculty.query.all())
    chosen_elective_id = tmp.elective_id
    return render_template('ChooseElectiveToOffer.html', title='Choose Elective to Offer', electives = electives, choice = chosen_elective_id)

#Faculty Role: GET method endpoint that updates the Faculty's choice in the Databse.
#A "None" entry indicates faculty hasn't chosen a course yet
@bp.route('/funcChooseElectiveToOffer/<elective_id>')
@requires_role('Faculty')
def funcChooseElectiveToOffer(elective_id):
    tmp = InitialElectiveList.query.filter_by(electiveID=elective_id).first()
    if (tmp is None) and elective_id != 'None':
        flash("Invalid Elective ID, cannot be chosen")
        return(redirect(url_for('main.index')))
    else:
        tmp = Faculty.query.filter_by(user_id=int(current_user.id)).first()
        tmp.elective_id = str(elective_id)
        db.session.commit()
        print("User has chosen ", elective_id)
        return(redirect(url_for('main.chooseElectiveToOffer')))


@bp.route('/ViewFacultyChoice')
@login_required
# @requires_role('Faculty')
def viewFacultyChoice():
    tmp = InitialElectiveList.query.all()
    tmp_list = []
    for x in tmp:
        tmp_list += [[x.electiveID, x.electiveName]]
    fac_list = {}

    # Consider changing logic to JOIN    
    for x in tmp_list:
        f = Faculty.query.filter_by(elective_id = x[0]).all()
        med_list = []
        for y in f:
            med = FacultyDetails.query.filter_by(fac_id = y.fac_id).first()
            med_list += [[med.name, med.fac_id]]
        fac_list[x[0]] = {'name' : x[1], 'faculty': med_list}
    
    print(fac_list)


    return render_template('ViewFacultyChoice2.html', title='Electives Chosen by Faculty', fac_list = fac_list)

@bp.route('/generateListv2')
@requires_role('Chairperson')
def generateListv2():
    data = read_json()
    if(data['FacultyOpen'] == 'True'):
        flash('Portal should be closed for Faculty before Consolidating the Electives')
        return(redirect(url_for('main.index')))
    ElectiveListv2.query.delete()
    db.session.commit()
    q = db.engine.execute("select electiveID from initial_elective_list")
    electives = []
    electivesV2 = []
    for x in q:
        electives += [x[0]]

    querystring = "Select count(*) from initial_elective_list, faculty where initial_elective_list.electiveID = faculty.elective_id and faculty.elective_id = '{}'"
    for x in electives:
        tmp = db.engine.execute(querystring.format(x))
        cnt = 0
        for row in tmp:
            cnt = row[0]

        if int(cnt) > 1:
            electivesV2 += [x]
        
    for x in electivesV2:
        a = InitialElectiveList.query.filter_by(electiveID = x).first()
        tmp1 = ElectiveListv2(electiveID = a.electiveID, electiveName = a.electiveName, electiveDescription = a.electiveDescription)
        db.session.add(tmp1)
        db.session.commit()

    data['v2gen'] = 'True'
    write_json(data)
    flash("Compiled Elective List Generated!!")
    return redirect(url_for('main.index'))

@bp.route('/scrapeConsolidatedList')
@requires_role('Chairperson')
def scrapeConsolidatedList():
    data = read_json()
    if(data['StudentOpen'] == 'True'):
        flash('Portal is currently open for Students, cannot Scrape the List!')
        return redirect(url_for('main.index'))
    elif (data['v3gen'] == 'True'):
        flash('Electives have already been allotted to Students! Cannot Scrape the List now!')
        return redirect(url_for('main.index'))
    else:
        ElectiveListv2.query.delete()
        db.session.commit()
        flash('Consolidated List has been Scraped')
        data['v2gen'] = 'False'
        write_json(data)
        return redirect(url_for('main.index'))

@bp.route('/test')
def test():
    data = read_json()
    data["FacultyOpen"] = "False"
    write_json(data)
    print(ElectiveListv2.query.all())
    return data

def read_json():
    dir = os.path.dirname(__file__)
    data = None
    with open(os.path.join(dir, "data.json"), "r") as f:
        data = f.read()
    return (json.loads(data))

def write_json(data):
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, 'data.json'), 'w+') as f:
        f.write(json.dumps(data))
    return

    
@bp.route('/ChooseElectiveToStudy')
@requires_role('Student')
def chooseElectiveToStudy():
    data = read_json()
    if(data["StudentOpen"] == 'False'):
        if(data['v2gen'] == 'False'):
            flash("The Electives List has not been prepared yet")
        elif(data['v3gen'] == 'True'):
            flash("Elective has already been allotted to you. You can no longer access this portal.")
        return(redirect(url_for('main.index')))

    electives = ElectiveListv2.query.all()
    tmp = Student.query.filter_by(user_id = current_user.id).first()

    choice = {'1': tmp.elective_id1, '2': tmp.elective_id2, '3': tmp.elective_id3}

    return render_template('ChooseElectiveToStudy.html', title='Choose Elective Preference', electives = electives, choice = choice)


@bp.route('/funcChooseElectiveToStudy/<elective_id>/<pref>')
@requires_role('Student')
def funcChooseElectiveToStudy(elective_id, pref):
    tmp = ElectiveListv2.query.filter_by(electiveID=elective_id).first()
    if (tmp is None) and elective_id != 'None':
        flash("Invalid Elective ID")
        return(redirect(url_for('main.index')))
    else:
        tmp = Student.query.filter_by(user_id=int(current_user.id)).first()
        if(pref == '1'):
            tmp.elective_id1 = str(elective_id)
        elif (pref == '2'):
            tmp.elective_id2 = str(elective_id)
        elif (pref == '3'):
            tmp.elective_id3 = str(elective_id)
        else:
            flash('Invalid Preference Number')
        db.session.commit()

        # print("User has chosen ", elective_id)
        return(redirect(url_for('main.chooseElectiveToStudy')))

@bp.route('/ViewCourseOfferingFaculty')
@login_required
@requires_role('Student')
def viewCourseOfferingFaculty():
    tmp = ElectiveListv2.query.all()
    tmp_list = []
    for x in tmp:
        tmp_list += [[x.electiveID, x.electiveName]]
    fac_list = {}

    # Consider changing logic to JOIN    
    for x in tmp_list:
        f = Faculty.query.filter_by(elective_id = x[0]).all()
        med_list = []
        for y in f:
            med = FacultyDetails.query.filter_by(fac_id = y.fac_id).first()
            med_list += [[med.name, med.fac_id]]
        fac_list[x[0]] = {'name' : x[1], 'faculty': med_list}
    print(fac_list)

    return render_template('ViewCourseOfferingFaculty.html', title='Electives Chosen by Faculty', fac_list = fac_list)

@bp.route('/ViewCourseOfferingFacultyCP')
@login_required
@requires_role('Chairperson')
def viewCourseOfferingFacultyCP():
    data = read_json()
    if(data['v2gen'] == 'False'):
        flash("Courses have not been assigned to Faculty yet!")
        return redirect(url_for('main.index'))

    tmp = ElectiveListv2.query.all()
    tmp_list = []
    for x in tmp:
        tmp_list += [[x.electiveID, x.electiveName]]
    fac_list = {}

    # Consider changing logic to JOIN    
    for x in tmp_list:
        f = Faculty.query.filter_by(elective_id = x[0]).all()
        med_list = []
        for y in f:
            med = FacultyDetails.query.filter_by(fac_id = y.fac_id).first()
            med_list += [[med.name, med.fac_id]]
        fac_list[x[0]] = {'name' : x[1], 'faculty': med_list}
    print(fac_list)

    return render_template('ViewCourseOfferingFaculty.html', title='Electives Chosen by Faculty', fac_list = fac_list)

@bp.route('/FacultyPortal/<status>')
@requires_role('Chairperson')
def FacultyPortal(status):
    data = read_json()
    data["FacultyOpen"] = status
    v2gen=data['v2gen']

    if(v2gen == 'True'):
        flash('Consolidated Elective List has already been generated! Cannot Open the portal for Faculty again!')
        return redirect(url_for('main.index'))
        
    write_json(data)
    tmp = str(status)
    if(tmp=="True"):
        msg = "Faculty Portal is now Open"
    else:
        msg = "Faculty Portal is now Closed"
    flash(msg)
    return redirect(url_for('main.index'))

@bp.route('/StudentPortal/<status>')
@requires_role('Chairperson')
def StudentPortal(status):
    data = read_json()
    data["StudentOpen"] = status
    v3gen = data['v3gen']

    if(v3gen == 'True'):
        flash('Electives have already been allotted to Students! Cannot Open portal for Students again!')
        return redirect(url_for('main.index'))

    write_json(data)
    tmp = str(status)
    if(tmp=="True"):
        msg = "Student Portal is now Open"
    else:
        msg = "Student Portal is now Closed"
    flash(msg)
    return redirect(url_for('main.index'))


#Write Query to finish this off
@bp.route('/GenerateListv3')
@requires_role('Chairperson')
def generateListv3():

    data = read_json()
    
    if(data['StudentOpen'] == 'True' or data['FacultyOpen'] == 'True'):
        flash("Portal open for Students. Cannot Allot Electives!")
        return redirect(url_for('main.index'))

    else:
        flash("The final Elective Allotment List has been generated!")
        data['v3gen'] = 'True'
        write_json(data)
        return redirect(url_for('main.index'))


@bp.route('/ScrapeListv3')
@requires_role('Chairperson')
def scrapeListv3():
    data = read_json()
    
    flash("The Elective Allotment has been scraped!")
    data['v3gen'] = 'False'
    write_json(data)
    return redirect(url_for('main.index'))

@bp.route('/ElectiveAllottedList')
@requires_role('Chairperson')
def ElectiveAllottedList():
    data = read_json()
    if(data['v3gen'] == 'True'):
        tmp = Student.query.all()
        tmp2 = ElectiveListv2.query.all()
        M = {}
        for x in tmp2:
            M[x.electiveID] = x.electiveName
        return render_template('viewAlloted.html', title='Elective Allotment List', M = M, students = tmp) 
    else:
        flash('Electives not yet allotted!')
        return redirect(url_for('main.index'))

@bp.route('/ViewFacultyChoice2')
@requires_role('Thavaru')
def viewFacultyChoice2():
    tmp_list = Faculty.query.all()
    fac_list = []

    # Consider changing logic to JOIN    
    for x in tmp_list:
        f = FacultyDetails.query.filter_by(fac_id = x.fac_id).first()
        name = f.name
        fac_id = f.fac_id
        elective = x.elective_id
        if elective != "None":
            elective = elective + " : " + (InitialElectiveList.query.filter_by(electiveID = x.elective_id).first()).electiveName
        fac_list.append({"name" : name, "fac_id" : fac_id, "elective" : elective})

    return render_template('ViewFacultyChoice_OldTemplate.html', title='Electives Chosen by Faculty', fac_list = fac_list)