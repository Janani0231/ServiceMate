from flask import Flask, render_template, request, redirect, url_for, flash, session
from extensions import db, login_manager
from model import User
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = Flask(__name__, static_folder='static')

app.config.from_object('config.DevelopmentConfig')
db.init_app(app)
login_manager.init_app(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


from model import *
from routes import *

if __name__ == '__main__':
    app.run(port=8000)