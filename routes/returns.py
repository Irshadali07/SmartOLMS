from flask import Blueprint, render_template, redirect, session, request
from models import db, Issue, Book, User
from datetime import datetime

return_bp = Blueprint('return_bp', __name__)

# PAGE
@return_bp.route('/returns')
def return_page():
    if 'user' not in session:
        return redirect('/')

    search = request.args.get('search', '')

    if search:
        issues = Issue.query.join(User).filter(
            User.username.ilike(f"%{search}%")
        ).all()
    else:
        issues = Issue.query.all()

    return render_template(
        'returns.html',
        issues=issues,
        user=session['user'],
        now=datetime.utcnow(),
        search=search   
    )

# ACTION
@return_bp.route('/return_book/<int:id>')
def return_book(id):
    issue = db.session.get(Issue, id)

    if issue:
        issue.return_date = datetime.utcnow()

        book = db.session.get(Book, issue.book_id)
        if book:
            book.available = True

        db.session.commit()

    return redirect('/returns')