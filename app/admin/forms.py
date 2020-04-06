from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Subject, Task


class SubjectForm(FlaskForm):
    """
    Form for admin to add or edit a subject
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class TaskForm(FlaskForm):
    """
    Form for admin to add or edit a task
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class StudentAssignForm(FlaskForm):
    """
    Form for admin to assign tasks and subjects to students
    """
    subject = QuerySelectField(query_factory=lambda: Subject.query.all(),get_label="name")
    task = QuerySelectField(query_factory=lambda: Task.query.all(),get_label="name")
    submit = SubmitField('Submit')