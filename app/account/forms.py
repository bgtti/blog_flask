# Account information form

from flask_wtf import FlaskForm  
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField  
from wtforms.validators import DataRequired, Length  


class The_Accounts(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about = TextAreaField("About", validators=[Length(max=385)])
    picture = FileField("Profile picture")
    submit = SubmitField()
