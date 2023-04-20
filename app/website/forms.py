from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class The_Comments(FlaskForm):
    comment = TextAreaField("Comment", validators=[
                            DataRequired()], widget=TextArea())
    submit = SubmitField()
