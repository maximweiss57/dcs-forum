from flask import Flask, Blueprint,url_for
from flask_login import LoginManager
from models import Users
from instance import db
from routes import routes_bp

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

    app.config["SECRET_KEY"] = 'dcs-forum'
    app.config["TESTING"] = testing
    app.config["DEBUG"] = True

    if testing :
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test-dcsforum.db'
    else:
        app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql+mysqlconnector://root:root@db/dcsforum'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
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






