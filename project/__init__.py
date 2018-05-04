from flask import Flask
from flask_pymongo import PyMongo


UPLOAD_FOLDER = '/home/corey/Desktop/efolder/project/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

mongo = PyMongo(app)

from project import routes
