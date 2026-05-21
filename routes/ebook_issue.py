from flask import Blueprint, render_template, request, redirect, session
from models import db, ebook, ebook_issue, User
from datetime import datetime

ebook_issue_bp = Blueprint('ebook_issue_bp', __name__)

# PAGE
@ebook_issue_bp.route('/ebook_issue')
def ebook_issue_page():
    if 'user' not in session:
        return redirect('/')

    books = ebook.query.all()
    issues = ebook_issue.query.all()
    users = User.query.all()   # 🔥 MISSING THA

    return render_template(
        'ebook_issue.html',
        books=books,
        issues=issues,
        users=users,   # 🔥 ADD KIYA
        user=session['user']
    )


# ISSUE
@ebook_issue_bp.route('/issue_ebook', methods=['POST'])
def issue_ebook():
    user_id = request.form['user_id']
    ebook_id = request.form['ebook_id']

    issue = ebook_issue(
        user_id=user_id,
        ebook_id=ebook_id,
        issue_date=datetime.utcnow()
    )

    db.session.add(issue)
    db.session.commit()

    return redirect('/ebook_issue')


# RETURN
@ebook_issue_bp.route('/return_ebook/<int:id>')
def return_ebook(id):
    issue = db.session.get(ebook_issue, id)

    if issue:
        issue.return_date = datetime.utcnow()
        db.session.commit()

    return redirect('/ebook_issue')