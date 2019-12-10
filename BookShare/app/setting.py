import os
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Gets the absolute path to the current file
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "app.db")

SQLALCHEMY_TRACK_MODIFICATIONS = True


