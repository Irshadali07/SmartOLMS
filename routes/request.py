from flask import Blueprint, render_template, request, redirect, session
from models import db, Request, User

request_bp = Blueprint('request_bp', __name__)

# 🔹 USER: Send Book Request
@request_bp.route('/request-book', methods=['POST'])
def request_book():
    if 'user' not in session:
        return redirect('/')

    book_name = request.form['book_name']

    user = User.query.filter_by(username=session['user']).first()

    new_request = Request(
        user_id=user.id,
        book_name=book_name,
        status="Pending"
    )

    db.session.add(new_request)
    db.session.commit()

    return redirect('/dashboard')


# 🔹 ADMIN: View All Requests
@request_bp.route('/requests')
def view_requests():
    if 'user' not in session:
        return redirect('/')

    requests = Request.query.all()

    return render_template(
        'requests.html',
        requests=requests,
        user=session['user']
    )


# 🔹 ADMIN: Approve Request
@request_bp.route('/approve/<int:id>')
def approve_request(id):
    req = Request.query.get(id)

    if req:
        req.status = "Approved"
        db.session.commit()

    return redirect('/requests')


# 🔹 ADMIN: Reject Request
@request_bp.route('/reject/<int:id>')
def reject_request(id):
    req = Request.query.get(id)

    if req:
        req.status = "Rejected"
        db.session.commit()

    return redirect('/requests')