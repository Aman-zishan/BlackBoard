from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Subject, Task


class SubjectForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class TaskForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class StudentAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    subject = QuerySelectField(query_factory=lambda: Subject.query.all(),get_label="name")
    task = QuerySelectField(query_factory=lambda: Task.query.all(),get_label="name")
    submit = SubmitField('Submit')