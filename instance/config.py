import os

MONGO_DBNAME = os.environ['MONGO_DBNAME']
MONGO_URI = os.environ['MONGO_URI']

SECRET_KEY = os.environ['SECRET_KEY']
WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']
