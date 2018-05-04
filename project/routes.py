import os
from flask import render_template, request, redirect, url_for
from project import app, forms
from werkzeug.utils import secure_filename
from . import mongo
from bson.objectid import ObjectId

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
        data.pop('csrf_token', None)

        result = mongo.db.efolder_data.insert_one(data)
        print(result.inserted_id)

        if filename:
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
    table_data = mongo.db.efolder_data.find()
    return render_template('view.html', title='E-Folder - View', table_data = table_data)


@app.route('/create')
def create():
    return render_template('create.html', title='E-Folder - Create')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
