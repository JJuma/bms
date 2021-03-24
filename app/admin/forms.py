from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Rooms, Nodes, Sensors, Controllers


class RoomsForm(FlaskForm):
    """
    Form for admin to add or edit a Rooms
    """
    id = StringField('ID', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NodesForm(FlaskForm):
    """
    Form for admin to add or edit a Nodes
    """
    id = StringField('ID', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SensorsForm(FlaskForm):
    """
    Form for admin to add or edit a Sensors
    """
    id = StringField('ID', validators=[DataRequired()])
    node = StringField('Node', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ControllersForm(FlaskForm):
    """
    Form for admin to add or edit a Controllers
    """
    id = StringField('ID', validators=[DataRequired()])
    node = StringField('Node', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
