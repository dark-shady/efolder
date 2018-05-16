import os
from flask import render_template, request, redirect, url_for
from project import app, forms
from werkzeug.utils import secure_filename
from . import mongo
from bson.objectid import ObjectId
import datetime

def userid_to_name(userid):
    result = mongo.db.users.find_one({'userid':userid})
    return result['name']
app.add_template_global(userid_to_name, name='userid_to_name')


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='E-Folder')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = forms.AddForm()

    if form.validate_on_submit():
        print("Validating")
        # check if the post request has the file part
        file = None
        if 'uploadfile' in request.files:
            file = request.files['uploadfile']

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

            else:
                form.uploadfile.errors = ['This is not an allowed file type']
                return render_template('add.html', title='E-Folder - Add', form=form)

        print("Inserting")
        data = request.form.to_dict()

        # Add current datetime to dict
        data['datetime'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M")

        # Remove CSRF token from dict
        data.pop('csrf_token', None)

        # Actually submit data to mongodb
        result = mongo.db.efolder_data.insert_one(data)

        # If file attachedd, edit db entry to include filename
        if file:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], str(result.inserted_id)))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(result.inserted_id), filename))
            mongo.db.efolder_data.update({"_id": ObjectId(result.inserted_id)},
                                         {
                                         "$set": {"filename":filename}
                                         })

        return redirect(url_for('view'))
    else:
        return render_template('add.html', title='E-Folder - Add', form=form)


@app.route('/view')
def view():
    table_data = mongo.db.efolder_data.find().sort('datetime',-1)

    return render_template('view.html', title='E-Folder - View', table_data = table_data)


@app.route('/create')
def create():
    return render_template('create.html', title='E-Folder - Create')


@app.route('/search/<searchterm>')
@app.route('/search', methods=['POST'])
def search(searchterm=None):
    if request.method == "POST":
         searchterm = request.form['searchterm']
    if searchterm:
        query = {
            "$or": [
                {
                    "designator": { "$regex": searchterm, "$options": "i" }
                },
                {
                    "serialnumber": { "$regex": searchterm, "$options": "i" }
                },
                {
                    "partnumber": { "$regex": searchterm, "$options": "i" }
                },
                {
                    "notes": { "$regex": searchterm, "$options": "i" }
                },
                {
                    "product": { "$regex": "^" + searchterm + "$", "$options": "i" }
                }
            ]
        }
        table_data = mongo.db.efolder_data.find(query).sort('datetime',-1)
    else:
        table_data = mongo.db.efolder_data.find().sort('datetime',-1)

    return render_template('search.html', title='E-Folder - Search', searchterm= searchterm, table_data = table_data)


@app.route('/edit/<entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    error_msg = ""
    #Check if entry_id is correct format
    if not ObjectId.is_valid(entry_id):
        error_msg = "This is not a valid entry ID format"

    result = mongo.db.efolder_data.find_one({"_id": ObjectId(entry_id)})
    #Check if entry ID exists in DB
    if result == None:
        error_msg = "This is not a valid entry ID"

    if error_msg:
        return render_template('error.html', error_msg = error_msg)

    #Create form - remove userid and add entry_id
    result.pop('userid')
    result['entry_id'] = entry_id
    form = forms.EditForm(data=result)
    if request.method == "POST" and form.validate():
        #Validating submitted information
        print("Validating")

        mongo.db.efolder_data.update_one({"_id":ObjectId(form.entry_id.data)},
                                           {"$set":
                                             {"product":form.product.data,
                                             "serialnumber":form.serialnumber.data,
                                             "partnumber":form.partnumber.data,
                                             "designator":form.designator.data,
                                             "notes":form.notes.data
                                             }
                                           })

        return render_template('index.html')
    else:
        return render_template('edit.html',  title='E-Folder - Edit', form=form, entry_id=entry_id)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
