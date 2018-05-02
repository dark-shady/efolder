from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email

class AddForm(FlaskForm):
    userid = StringField("User ID: ", validators=[DataRequired()])
    product = SelectField("Product: ", validators=[DataRequired()],
              choices=[('oneview', 'Oneview')])
    partnumber = StringField("User ID: ")
    serialnumber = StringField("User ID: ")
    designator = StringField("User ID: ")
    notes = TextAreaField("Note:", validators=[DataRequired()])
    uploadfile = FileField()
    submit = SubmitField("Submit")
