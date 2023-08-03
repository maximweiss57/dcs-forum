from flask import Flask,render_template
from flask_mysqldb import MySQL


app=Flask(__name__)
@app.route('/')
def start():
    return render_template('index.html')