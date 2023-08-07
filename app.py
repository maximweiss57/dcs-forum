from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index2():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'password':
        return redirect('/')
    else:
        return render_template('login.html', error='Invalid username or password.')

@app.route('/register')
def register():
    return render_template('register.html')