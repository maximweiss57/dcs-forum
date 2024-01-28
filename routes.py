from flask import render_template, request, redirect, Blueprint,url_for, flash
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
        except:
            print("user registration failed")
            return 'There was an issue with the registration process'
        return redirect('/login')
    else:
        return render_template('register.html')

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@routes_bp.route('/forums')
def forums():
    return render_template('Forums.html', current_user=current_user)

@routes_bp.route('/downloads', methods=['GET'])
def downloads():
    return render_template(
        'downloads.html', current_user=current_user, download=Download.query.order_by(Download.created_at).all())

@routes_bp.route('/create_download', methods=['POST', 'GET'])
def create_download():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        link = request.form['link']
        created_at = datetime.utcnow()
        new_download = Download(
            name=name, description=description, link=link, created_at=created_at)
        try:
            db.session.add(new_download)
            db.session.commit()
            return render_template('downloads.html', current_user=current_user, new_download=new_download)
        except:
            return 'There was an issue with the upload process'
    else:
        return render_template('create_download.html')

@routes_bp.route('/events')
def events():
    return render_template('events.html', current_user=current_user)

@routes_bp.route('/squadrons', methods=['POST', 'GET'])
def squadrons():
    squadrons = Squadrons.query.order_by(Squadrons.created_at).all()
    return render_template('squadrons.html', squadrons=squadrons, current_user=current_user)

@routes_bp.route('/squadrons_reg', methods=['POST', 'GET'])
def squadrons_reg():
    if request.method == 'POST':
        print("0")
        name = request.form['name']
        description = request.form['description']
        members_input = request.form['members']
        created_at = request.form['created_at']
        created_at = datetime.strptime(created_at, '%Y-%m-%d').date()
        members_list = members_input.split(',')

        existing_squadron = Squadrons.query.filter_by(name=name).first()
        if existing_squadron:
            return 'A squadron with the same name already exists. Please choose a different name.'

        new_squadron = Squadrons(
            name=name, description=description, created_at=created_at)
        members = Users.query.filter(Users.username.in_(members_list)).all()
        new_squadron.members = members

        try:
            db.session.add(new_squadron)
            db.session.commit()
            new_squadron.members = members  # Assign the members directly
            db.session.commit()
            return redirect(url_for('routes_bp.squadrons'))
        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            return 'There was an issue with the squadron registration process'

    else:
        return render_template('squadrons_reg.html')
    
@routes_bp.route('/admin', methods=['GET'])
def admin():
    is_admin = current_user.is_admin

    if not is_admin:
        flash("Access denied. You are not an admin.", "error")
        return redirect(url_for('routes_bp.index'))

    try:
        from sqlalchemy.orm import joinedload

        all_users = Users.query.filter(Users.username != 'admin').with_entities(
    Users.id, Users.username, Users.email, Users.password, Users.squadron_id)

        return render_template('admin.html', is_admin=is_admin, all_users=all_users)
    except Exception as e:
        flash("An error occurred while retrieving user data.", "error")
        return redirect(url_for('routes_bp.index'))


@routes_bp.route('/leave_squadron', methods=['GET'])
def leave_squadron():
    current_user.squadron = None
    db.session.commit()
    return redirect('/profile')

from flask import render_template, request, redirect, url_for

@routes_bp.route('/join_squadron/<int:squadron_id>', methods=['GET','POST'])
def join_squadron(squadron_id):
    squadron = Squadrons.query.get(squadron_id)  
    current_user.squadron = squadron
    db.session.commit()

    return redirect(url_for('routes_bp.squadrons'))

@routes_bp.route('/delete_squadron/<int:squadron_id>', methods=['GET', 'POST'])
def delete_squadron(squadron_id):
    squadron = Squadrons.query.get(squadron_id)
    if squadron:
        if current_user.is_admin:
            try:
                db.session.delete(squadron)
                db.session.commit()
                flash('Squadron deleted successfully', 'success,refresh page for updates to take place')
                
            except Exception as e:
                db.session.rollback()
    else:
        flash('Squadron not found', 'error')

    return redirect(url_for('routes_bp.squadrons'))