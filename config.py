import os

status = ''


class Config:
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    status = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev-dcsforum.db'


class ProductionConfig(Config):
    status = 'production' 
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@host/dbname'
