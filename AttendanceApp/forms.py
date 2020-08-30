from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length

class RollNoForm(FlaskForm):
    rollNo = StringField('Roll No', validators=[DataRequired(), Length(min=2, max=20)])
    
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')

class AdminForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember me')

    submit = SubmitField('Login')