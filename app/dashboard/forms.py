
from datetime import datetime
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class The_Posts(FlaskForm):
    theme = SelectField(u'Theme', choices=[
                        'Beach', 'City', 'Nature', 'Culture'])
    author = StringField("Author")
    date = DateTimeField('Date', default=datetime.now, format='%Y-%m-%d')
    title = StringField("Title", validators=[DataRequired()])
    intro = StringField("Intro", validators=[DataRequired()])
    body = CKEditorField("Body", validators=[DataRequired()])
    picture_v = StringField(
        "Picture Vertical", default="Picture_v_XX.jpg", validators=[DataRequired()])
    picture_v_source = StringField("Picture Vertical", default="http://")
    picture_h = StringField(
        "Picture Horizontal", default="Picture_h_XX.jpg", validators=[DataRequired()])
    picture_h_source = StringField("Picture Vertical", default="http://")
    picture_s = StringField(
        "Picture Squared", default="Picture_s_XX.jpg", validators=[DataRequired()])
    picture_s_source = StringField("Picture Vertical", default="http://")
    # picture_s = FileField("Picture Squared")
    # picture_s_source = StringField("Picture Vertical", default="http://")
    picture_alt = StringField("Picture Alt Text", validators=[DataRequired()])
    meta_tag = StringField("Meta Tag", validators=[DataRequired()])
    title_tag = StringField("Title Tag", validators=[DataRequired()])
    submit = SubmitField()
