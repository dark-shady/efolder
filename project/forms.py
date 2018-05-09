from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField, ValidationError
from wtforms.validators import DataRequired, Email
from . import mongo


def check_userid(form, field):
    if mongo.db.users.find_one({"userid":field.data}):
        print("User exists!")
        return True
    raise ValidationError('User ID doesn\'t exist')
    return False


class AddForm(FlaskForm):
    userid = StringField("User ID: ", validators=[DataRequired(), check_userid])
    product = SelectField("Product: ", validators=[DataRequired()],
              choices=[('Oneview', 'Oneview'),
                       ('K2', 'K2'),
                       ('K3', 'K3'),
                       ('Rio', 'Rio'),
                       ('Quantum', 'Quantum'),
                       ('Orius', 'Orius'),
                       ('GIB', 'GIB'),
                       ('Abruzzi', 'Abruzzi'),
                       ('Digiscan', 'Digiscan'),
                       ('Sensor', 'Sensor')])
    partnumber = StringField("Part Number: ")
    serialnumber = StringField("Serial Number: ")
    designator = StringField("Designator: ")
    notes = TextAreaField("Note:", validators=[DataRequired()])
    uploadfile = FileField("Attachment: ")
    submit = SubmitField("Submit")
