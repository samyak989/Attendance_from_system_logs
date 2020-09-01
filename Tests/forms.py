from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

class RollNoForm(FlaskForm):
    rollNo = StringField('Roll No', validators=[DataRequired(), Length(min=2, max=20)])
    
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    date = DateField('Date', format= '%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField('Show Records')

class DownloadForm(FlaskForm):

    submit = SubmitField('Download Form')