from datetime import datetime
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class The_Posts(FlaskForm):
    theme = SelectField(u'Theme', coerce=int)
    author = StringField("Author")
    date = DateTimeField('Date', default=datetime.now, format='%Y-%m-%d')
    title = StringField("Title", validators=[DataRequired()])
    intro = StringField("Intro", validators=[DataRequired()])
    body = CKEditorField("Body", validators=[DataRequired()])

    picture_v = FileField("Picture Vertical")
    picture_v_source = StringField(
        "Picture Vertical Source", default="http://")
    picture_v_size = StringField("Picture File Size")

    picture_h = FileField("Picture Horizontal")
    picture_h_source = StringField(
        "Picture Horizontal Source", default="http://")
    picture_h_size = StringField("Picture File Size")

    picture_s = FileField("Picture Squared")
    picture_s_source = StringField("Picture Squared Source", default="http://")
    picture_s_size = StringField("Picture File Size")
    
    picture_alt = StringField("Picture Alt Text", validators=[DataRequired()])
    meta_tag = StringField("Meta Tag", validators=[DataRequired()])
    title_tag = StringField("Title Tag", validators=[DataRequired()])
    submit = SubmitField()
