import os

status = ''


class Config:
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    status = 'development'  # Set the status for this configuration
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev-dcsforum.db'


class TestingConfig(Config):
    status = 'testing'  # Set the status for this configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test-dcsforum.db'


class ProductionConfig(Config):
    status = 'production'  # Set the status for this configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@host/dbname'
