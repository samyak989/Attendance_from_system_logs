from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class RollNoForm(FlaskForm):
    rollNo = StringField('Roll No', validators=[DataRequired(), Length(min=2, max=20)])
    
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    date = DateField('Date', format= '%Y-%m-%d', validators=[DataRequired()])

    fromTime = TimeField('From', validators= [DataRequired()], default= datetime.fromisoformat('2020-01-01T10:00:00'))
    toTime = TimeField('To', validators= [DataRequired()], default= datetime.fromisoformat('2020-01-01T17:00:00'))

    submit = SubmitField('Show Records')

class DownloadForm(FlaskForm):

    submit = SubmitField('Download CSV')