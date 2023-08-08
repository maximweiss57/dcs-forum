from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dcs-forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dcs-forum'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/index.html')
def index2():
    return render_template('index.html', current_user=current_user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                return redirect('/index.html')
            else:
                return 'Wrong password'
        else:
            return 'User not found'
    else:
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = Users(username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return 'There was an issue with the registration process'
        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index.html')

@app.route('/forums')
def forums():
    return render_template('forums.html', current_user=current_user)

@app.route('/downloads')
def downloads():
    return render_template('downloads.html', current_user=current_user)

@app.route('/events')
def events():
    return render_template('events.html', current_user=current_user)

@app.route('/squadrons')
def squadrons():
    return render_template('squadrons.html', current_user=current_user)

