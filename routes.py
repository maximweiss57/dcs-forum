from flask import render_template, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from models import Users, Squadrons, Download
from datetime import datetime
from instance import db
from app_running_conf import app


@app.route('/')
def index():
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

                return render_template('index.html', current_user=current_user)

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
    return redirect('/')


@app.route('/forums')
def forums():
    return render_template('forums.html', current_user=current_user)


@app.route('/downloads', methods=['GET'])
def downloads():
    return render_template(
        'downloads.html', current_user=current_user, download=Download.query.order_by(Download.created_at).all())


@app.route('/create_download', methods=['POST', 'GET'])
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


@app.route('/events')
def events():
    return render_template('events.html', current_user=current_user)


@app.route('/squadrons', methods=['POST', 'GET'])
def squadrons():
    squadrons = Squadrons.query.order_by(Squadrons.created_at).all()
    return render_template('squadrons.html', squadrons=squadrons, current_user=current_user)


@app.route('/squadrons_reg', methods=['POST', 'GET'])
def squadrons_reg():
    print("inside routeøß")
    if request.method == 'POST':
        print("0")
        name = request.form['name']
        description = request.form['description']
        members_input = request.form['members']
        created_at = request.form['created_at']
        created_at = datetime.strptime(created_at, '%Y-%m-%d').date()
        members_list = members_input.split(',')
        new_squadron = Squadrons(
            name=name, description=description, created_at=created_at)
        members = Users.query.filter(Users.username.in_(members_list)).all()
        new_squadron.members = members

        try:
            db.session.add(new_squadron)
            db.session.commit()
            for member in members:
                member.squadron = new_squadron.id
            db.session.commit()
            return redirect('/squadrons')
        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            return 'There was an issue with the squadron registration process'
    else:
        return render_template('squadrons_reg.html')


@app.route('/admin', methods=['GET'])
def admin():
    is_admin = current_user.is_admin

    if is_admin:
        all_users = Users.query.filter(Users.username != 'admin').all()
        return render_template('admin.html', is_admin=is_admin, all_users=all_users)
    else:
        return "Access denied. You are not an admin."


@app.route('/profile', methods=['GET'])
def profile():
    return render_template(
        'profile.html', current_user=current_user)
