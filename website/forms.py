from flask_wtf import FlaskForm
from wtforms import StringField,    DecimalField,      SubmitField, IntegerField, SelectField, PasswordField
from wtforms.validators import InputRequired,NumberRange , EqualTo
import sqlite3 as sql

data = sql.connect("data.sqlite")
db = data.cursor()

class RegistrationForm(FlaskForm):
    user_id = StringField("Username: ", validators=[InputRequired()])
    password = StringField("Password: " , validators=[InputRequired()])
    password2 = StringField("Confirm Password: " , validators=[InputRequired("Field required"),EqualTo("password",message="passwords do not match")])
    submit = SubmitField("Submit:")

class LoginForm(FlaskForm):
    user_id = StringField("Username: ", validators=[InputRequired()])
    password = StringField("Password: " , validators=[InputRequired()])
    submit = SubmitField("Submit:")





