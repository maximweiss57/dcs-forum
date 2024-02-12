from flask import Flask, Blueprint
from flask_login import LoginManager
from models import Users
from instance import db
from routes import routes_bp
import os

def create_admin_user(app):
    admin_username = "admin"
    admin_password = "admin"
    with app.app_context():
        existing_admin = Users.query.filter_by(username=admin_username).first()

    if existing_admin is None:
        admin = Users(username=admin_username, email='admin@admin.com',
                      password=admin_password, is_admin=True)
        db.session.add(admin)
        db.session.commit()

def create_app(testing):
        
    app = Flask(__name__)
    if testing :
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test-dcsforum.db'
        app.config["SECRET_KEY"] = 'dcs-forum'
    else: 
        app.config["SECRET_KEY"] = 'dcs-forum'
        app.config["DEBUG"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        POSTGRES_USER= "postgres"
        POSTGRES_PASSWORD= "root"
        POSTGRES_HOST = "db"
        POSTGRES_DB= "forum"
        db_port = "5432"
        db_uri = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{db_port}/{POSTGRES_DB}"
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)
    app.register_blueprint(routes_bp)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        create_admin_user(app)
    return app






