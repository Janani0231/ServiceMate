from flask import Flask ,render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run()