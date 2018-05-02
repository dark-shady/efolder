import os
from flask import render_template, request, redirect, url_for
from project import app, forms
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo


mongo = PyMongo(app)


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='E-Folder')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = forms.AddForm()

    if form.validate_on_submit():
        # check if the post request has the file part
        file = None
        if 'file' in request.files:
            file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
