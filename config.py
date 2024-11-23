from dotenv import load_dotenv
import os
load_dotenv()
class Config(object):
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')