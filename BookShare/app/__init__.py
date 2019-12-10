# -*- coding: UTF-8 -*-
# Converts all strings that appear explicitly in the module to unicode types
from __future__ import unicode_literals

from flask import Flask

# Importing SQLAlchemy into our application
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)

# Auto-save update
app.config['TEMPLATES_AUTO_RELOAD'] = True
# open debug model
app.config.update(DEBUG=True)


app.config.from_object('app.setting')

bootstrap = Bootstrap(app)

app.secret_key = app.config["SECRET_KEY"]

# The database URI for the connection

# Auto commit saves every commit and returns None with id as soon as the data object is added
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN '] = True

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "web.login"

from app.web import web_bp
app.register_blueprint(web_bp)

