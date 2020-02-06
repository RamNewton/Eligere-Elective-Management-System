#Importing modules used for creating Form objects
from flask_wtf import FlaskForm

#Importing classes for various fileds in forms
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.widgets import TextArea

#Importing validators
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Required

#Importing table models from DataBase
from app.models import InitialElectiveList, User
import re

#Form used by Chairperson to add Electives to the System
class AddElectives(FlaskForm):
    elective_id = StringField("Elective ID", validators = [DataRequired()])
    elective_name = StringField("Elective Name", validators = [DataRequired()])
    elective_description = StringField("Elective Description", widget = TextArea(), validators = [DataRequired()])
    submit = SubmitField('Submit Elective')

    def validate_elective_id(self, elective_id):
        tmp = InitialElectiveList.query.filter_by(electiveID=elective_id.data).first()
        
        pat = re.compile("^[A-Z]{3}[0-9]{3}$")

        if pat.match(elective_id.data) is None:
            raise ValidationError('Elective ID is in unexpected form.\nShould be like CSEXXX')

        if tmp is not None:
            raise ValidationError('Please enter a different elective id.')
        