from flask import render_template, request, redirect, Blueprint, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import Users, Squadrons, Download
from datetime import datetime
from instance import db

routes_bp = Blueprint('routes_bp', __name__, url_prefix='/', template_folder='templates')

@routes_bp.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@routes_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('routes_bp.index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('routes_bp.login'))
    return render_template('login.html')

@routes_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = Users(username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect(url_for('routes_bp.login'))
        except Exception as e:
            print("User registration failed:", e)
            flash('Failed to register user', 'error')
            return redirect(url_for('routes_bp.register'))
    return render_template('register.html')

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('routes_bp.index'))

@routes_bp.route('/forums')
def forums():
    return render_template('Forums.html', current_user=current_user)

@routes_bp.route('/downloads', methods=['GET'])
def downloads():
    downloads = Download.query.order_by(Download.created_at).all()
    return render_template('downloads.html', current_user=current_user, downloads=downloads)

@routes_bp.route('/create_download', methods=['POST', 'GET'])
@login_required
def create_download():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        link = request.form['link']
        new_download = Download(name=name, description=description, link=link)
        try:
            db.session.add(new_download)
            db.session.commit()
            flash('Download created successfully', 'success')
            return redirect(url_for('routes_bp.downloads'))
        except Exception as e:
            print("Error creating download:", e)
            flash('Failed to create download', 'error')
            return redirect(url_for('routes_bp.create_download'))
    return render_template('create_download.html')

@routes_bp.route('/events')
def events():
    return render_template('events.html', current_user=current_user)

@routes_bp.route('/squadrons', methods=['POST', 'GET'])
def squadrons():
    squadrons = Squadrons.query.order_by(Squadrons.created_at).all()
    return render_template('squadrons.html', squadrons=squadrons, current_user=current_user)

@routes_bp.route('/squadrons_reg', methods=['POST', 'GET'])
@login_required
def squadrons_reg():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        created_at = request.form['created_at']
        created_at = datetime.strptime(created_at, '%Y-%m-%d').date()
        new_squadron = Squadrons(name=name, description=description, created_at=created_at)
        try:
            db.session.add(new_squadron)
            db.session.commit()
            flash('Squadron registered successfully', 'success')
            return redirect(url_for('routes_bp.squadrons'))
        except Exception as e:
            print("Error registering squadron:", e)
            flash('Failed to register squadron', 'error')
            return redirect(url_for('routes_bp.squadrons_reg'))
    else:
        return render_template('squadrons_reg.html')
    
@routes_bp.route('/admin', methods=['GET'])
@login_required
def admin():
    if not current_user.is_admin:
        flash("Access denied. You are not an admin.", "error")
        return redirect(url_for('routes_bp.index'))
    
    try:
        all_users = Users.query.filter(Users.username != 'admin').with_entities(
            Users.id, Users.username, Users.email, Users.squadron_id)
        return render_template('admin.html', all_users=all_users)
    except Exception as e:
        print("Error in admin:", e)
        flash("An error occurred while retrieving user data.", "error")
        return redirect(url_for('routes_bp.index'))

@routes_bp.route('/leave_squadron', methods=['GET'])
@login_required
def leave_squadron():
    current_user.squadron = None
    db.session.commit()
    flash('Left squadron successfully', 'success')
    return redirect(url_for('routes_bp.profile'))

@routes_bp.route('/join_squadron/<int:squadron_id>', methods=['GET', 'POST'])
@login_required
def join_squadron(squadron_id):
    squadron = Squadrons.query.get(squadron_id)
    if squadron:
        current_user.squadron = squadron
        db.session.commit()
        flash('Joined squadron successfully', 'success')
    else:
        flash('Squadron not found', 'error')
    return redirect(url_for('routes_bp.squadrons'))

@routes_bp.route('/delete_squadron/<int:squadron_id>', methods=['GET', 'POST'])
@login_required
def delete_squadron(squadron_id):
    if not current_user.is_admin:
        flash('Access denied. You are not an admin.', 'error')
        return redirect(url_for('routes_bp.index'))

    squadron = Squadrons.query.get(squadron_id)
    if squadron:
        try:
            db.session.delete(squadron)
            db.session.commit()
            flash('Squadron deleted successfully', 'success')
        except Exception as e:
            db.session.rollback()
            print("Error deleting squadron:", e)
            flash('Failed to delete squadron', 'error')
    else:
        flash('Squadron not found', 'error')
    return redirect(url_for('routes_bp.squadrons'))


