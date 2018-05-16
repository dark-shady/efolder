from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField, ValidationError, HiddenField
from wtforms.validators import DataRequired
from . import mongo
from bson.objectid import ObjectId


def check_userid(form, field):
    if mongo.db.users.find_one({"userid":field.data}):
        return True
    raise ValidationError('User ID doesn\'t exist')
    return False

def check_userid_matches(form, field):
    if mongo.db.efolder_data.find_one({"$and":
                                    [
                                        {"userid":field.data},
                                        {"_id":ObjectId(form.entry_id.data)}
                                    ]}):
        return True
    raise ValidationError('User ID doesn\'t match User ID of person who submitted original entry.')
    return False

def valid_entry_id(form, field):
    if mongo.db.efolder_data.find_one({"_id":ObjectId(field.data)}):
        return True
    raise ValidationError('Not a valid entry ID')
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
                       ('Sensor', 'Sensor'),
                       ('Computer', 'Computer')])
    partnumber = StringField("Part Number: ")
    serialnumber = StringField("Serial Number: ")
    designator = StringField("Designator: ")
    notes = TextAreaField("Note:", validators=[DataRequired()])
    uploadfile = FileField("Attachment: ")
    submit = SubmitField("Submit")


class EditForm(FlaskForm):
    entry_id = HiddenField("Entry ID", validators=[DataRequired(), valid_entry_id])
    userid = StringField("User ID: ", validators=[DataRequired(), check_userid, check_userid_matches])
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
                       ('Sensor', 'Sensor'),
                       ('Computer', 'Computer')])
    partnumber = StringField("Part Number: ")
    serialnumber = StringField("Serial Number: ")
    designator = StringField("Designator: ")
    notes = TextAreaField("Note:", validators=[DataRequired()])
    uploadfile = FileField("Attachment: ")
    submit = SubmitField("Submit")
