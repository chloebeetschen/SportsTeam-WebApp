from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length
from .models import Member, Fixture, FixtureInfo


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password_hash = PasswordField('password_hash', validators=[DataRequired()])
    
    login = SubmitField('Login')

class ResetPass(FlaskForm):
    fname = StringField('name', validators=[DataRequired()])
    lname = StringField('lname', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password_hash = PasswordField('password_hash', validators=[DataRequired()])
    conf_password_hash = PasswordField('password_hash', validators=[DataRequired()])

    submit = SubmitField('Reset')
    
class MemberForm(FlaskForm):
    fname = StringField('name', validators=[DataRequired()])
    lname = StringField('lname', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password_hash = PasswordField('password_hash', validators=[DataRequired()])
    position = SelectField('position', choices=[('GK','GK'),('Defender','Defender'),('Midfielder','Midfielder'),('Winger','Winger'),('Striker','Striker'),], validators=[DataRequired()])
    
    submit = SubmitField('Join')

class ContactUsForm(FlaskForm):
    subject = StringField('subject', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])

    send = SubmitField('Submit')

class FixtureForm(FlaskForm):
    date = DateField('date', validators=[DataRequired()])
    team = StringField('team', validators=[DataRequired()])
    home_away = StringField('home_away', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    meet_loc = StringField('meet_loc', validators=[DataRequired()])
    time = StringField('time', validators=[DataRequired()])
    meet_time = StringField('meet_time', validators=[DataRequired()])

    choices = [(m.memberId,  m.fname + " " + m.lname) for m  in Member.query.order_by('position')]
    members = SelectMultipleField('members', coerce=int, choices=choices, validators=[DataRequired()])

    save = SubmitField('Save')
