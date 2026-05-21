from flask import Flask, render_template, request, redirect, session, flash
from models import db, User, Book, Issue, Request, ebook   
from datetime import datetime
import config

app = Flask(__name__, static_folder='../static')   
app.config.from_object(config)
app.config['SECRET_KEY'] = "secret123"

db.init_app(app)

# ---------------- LOGIN PAGE ----------------
@app.route('/')
def login_page():
    return render_template('login.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(
        username=request.form['username'],
        password=request.form['password']
    ).first()

    if user:
        session['user'] = user.username
        session['user_id'] = user.id
        return redirect('/home')

    return "Invalid Credentials ❌"


# ---------------- HOME ----------------
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('home.html', user=session['user'])


# ---------------- MY BOOKS ----------------
@app.route('/mybooks')
def mybooks():
    if 'user_id' not in session:
        return redirect('/')

    my_books = Issue.query.filter_by(user_id=session['user_id']).all()

    books_data = Book.query.all()
    total = len(books_data)
    issued = len([b for b in books_data if not b.available])
    available = total - issued

    return render_template(
        'mybooks.html',
        my_books=my_books,
        user=session['user'],
        now=datetime.utcnow(),
        total=total,
        issued=issued,
        available=available
    )


# ---------------- BOOKS ----------------
@app.route('/books')
def books():
    if 'user_id' not in session:
        return redirect('/')

    books = Book.query.all()
    return render_template('books.html', books=books, user=session['user'])


# ---------------- EBOOKS ----------------
@app.route('/ebooks')
def ebooks():
    if 'user_id' not in session:
        return redirect('/')

    ebooks_data = ebook.query.all()   # ✅ correct model
    return render_template('ebooks.html', books=ebooks_data, user=session['user'])


# ---------------- REQUEST BOOK (FIXED) ----------------
@app.route('/request/<int:book_id>')
def request_book(book_id):
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']
    book = Book.query.get(book_id)

    existing = db.session.query(Request).filter(
        Request.user_id == user_id,
        Request.book_name == book.title,
        Request.status.in_(["Pending", "Approved"])
    ).first()

    if existing:
        flash("Already requested this book ❌", "error")
        return redirect('/books')   # 👈 same page

    new_req = Request(
        user_id=user_id,
        book_name=book.title,
        status="Pending"
    )

    db.session.add(new_req)
    db.session.commit()

    flash("Request sent successfully ✅", "success")
    return redirect('/books?msg=1')

#approve request
@app.route('/approve/<int:id>')
def approve(id):
    req = Request.query.get(id)

    if req:
        req.status = "Approved"

        # 🔥 BOOK FIND
        book = Book.query.filter_by(title=req.book_name).first()

        # 🔥 ISSUE CREATE
        if book and book.available:
            issue = Issue(
                user_id=req.user_id,
                book_id=book.id
            )

            book.available = False

            db.session.add(issue)

        db.session.commit()

    return redirect('/requests')

#Reject request
@app.route('/reject/<int:id>')
def reject(id):
    req = Request.query.get(id)

    if req:
        req.status = "Rejected"
        db.session.commit()

    return redirect('/requests')

# ---------------- RETURN BOOK ----------------
@app.route('/return/<int:id>')
def return_book(id):
    if 'user_id' not in session:
        return redirect('/')

    issue = Issue.query.get(id)

    if issue and issue.user_id == session['user_id']:
        issue.return_date = datetime.utcnow()

        book = Book.query.get(issue.book_id)
        if book:
            book.available = True

        db.session.commit()

    return redirect('/mybooks')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5001)