from flask import Blueprint, render_template, request, redirect, session
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        session['user'] = username
        return redirect('/dashboard')
    return render_template('login.html', error="Invalid Credentials ❌")

@auth.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return redirect('/')

@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')