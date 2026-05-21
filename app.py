from flask import Flask, Request, render_template, session, redirect, request
from models import db, User, Book, Issue
from werkzeug.utils import secure_filename
from datetime import datetime
import config
from routes.returns import return_bp
from routes.users import users


# ---------------- CREATE APP ----------------
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

# ---------------- IMPORT BLUEPRINTS ----------------
from routes.auth import auth
from routes.books import books
from routes.issue import issue as issue_bp
from routes.users import users
from routes.ebook import ebook_bp
from routes.ebook_issue import ebook_issue_bp
from routes.request import request_bp

# ---------------- REGISTER BLUEPRINTS ----------------
app.register_blueprint(auth)
app.register_blueprint(books)
app.register_blueprint(issue_bp)
app.register_blueprint(users)
app.register_blueprint(return_bp)
app.register_blueprint(ebook_bp)
app.register_blueprint(ebook_issue_bp)
app.register_blueprint(request_bp)


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    books_data = Book.query.all()
    users_data = User.query.all()

    total = len(books_data)
    issued = len([b for b in books_data if not b.available])
    available = total - issued

    return render_template(
        'dashboard.html',
        books=books_data,
        users=users_data,
        total=total,
        issued=issued,
        available=available,
        user=session['user']
    )

# ---------------- BOOKS PAGE ----------------
@app.route('/books')
def books_page():
    if 'user' not in session:
        return redirect('/')

    books_data = Book.query.all()
    return render_template('books.html', books=books_data, user=session['user'])

# ---------------- ISSUE BOOK (FINAL CLEAN) ----------------
@app.route('/issue', methods=['POST'])
def issue_book():
    user_id = request.form['user_id']
    book_id = request.form['book_id']

    book = db.session.get(Book, book_id)

    if not book:
        return "Book not found ❌"

    if not book.available:
        return "Book already issued ❌"

    issue = Issue(
        user_id=user_id,
        book_id=book_id
    )

    book.available = False

    db.session.add(issue)
    db.session.commit()

    return redirect('/dashboard')

# ---------------- EDIT BOOK ----------------
@app.route('/edit_book/<int:id>', methods=['GET','POST'])
def edit_book(id):
    book = db.session.get(Book, id)

    if request.method == 'POST':
        book.title = request.form['title']

        # Image upload
        file = request.files.get('image')
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save("static/" + filename)
            book.image = filename  # ensure model has this field

        db.session.commit()
        return redirect('/books')

    return render_template('edit_book.html', book=book)


@app.route('/approve/<int:id>')
def approve(id):
    req = Request.query.get(id)

    if req:
        req.status = "Approved"

        # 🔥 book issue karna (auto)
        user = User.query.get(req.user_id)
        book = Book.query.filter_by(title=req.book_name).first()

        if book and book.available:
            issue = Issue(
                user_id=user.id,
                book_id=book.id
            )

            book.available = False

            db.session.add(issue)

        db.session.commit()

    return redirect('/requests')


@app.route('/reject/<int:id>')
def reject(id):
    req = Request.query.get(id)

    if req:
        req.status = "Rejected"
        db.session.commit()

    return redirect('/requests')


@app.route('/requests')
def requests_page():
    requests = Request.query.all()
    return render_template('requests.html', requests=requests) 


# ---------------- RUN ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)