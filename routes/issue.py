from flask import Blueprint, request, redirect, render_template, session
from models import db, Issue, Book, User
from datetime import datetime, timedelta

issue = Blueprint('issue', __name__)

# 🔥 PAGE ROUTE (GET)
@issue.route('/issue')
def issue_page():
    if 'user' not in session:
        return redirect('/')
    search = request.args.get('search', '')

    if search:
        users = User.query.filter(User.username.ilike(f"%{search}%")).all()
    else:
        users = User.query.all()

    books = Book.query.all()
    issues = Issue.query.all()   

    return render_template(
        'issue.html',
        books=books,
        users=users,
        issues=issues,   
        user=session['user']
    )


# 🔥 FORM SUBMIT (POST)
@issue.route('/issue_book', methods=['POST'])
def issue_book():
    user_id = request.form['user_id']
    book_id = request.form['book_id']

    book = db.session.get(Book, book_id)

    if not book or not book.available:
        return "Book not available ❌"

    issue = Issue(
        user_id=user_id,
        book_id=book_id,
        issue_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=7)  # 7 days rule
    )

    book.available = False

    db.session.add(issue)
    db.session.commit()

    return redirect('/issue')