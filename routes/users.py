from flask import Blueprint, render_template, request, redirect, session
from models import db, User

# Blueprint
users = Blueprint('users', __name__)

# USERS PAGE
@users.route('/users')
def users_page():
    if 'user' not in session:
        return redirect('/')

    all_users = User.query.all()

    return render_template(
        'users.html',
        users=all_users,
        user=session['user']
    )


# ➕ ADD USER
@users.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']

    existing = User.query.filter_by(username=username).first()
    if existing:
        return "User already exists "

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


# DELETE USER
@users.route('/delete_user/<int:id>')
def delete_user(id):
    user = db.session.get(User, id)

    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect('/users')