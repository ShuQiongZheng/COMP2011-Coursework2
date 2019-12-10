from flask import Blueprint

web_bp = Blueprint("web", __name__)

import app.web.views
