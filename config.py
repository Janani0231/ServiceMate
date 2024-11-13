from dotenv import load_dotenv
import os
load_dotenv()
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@hostname/dbname'