import os
from flask import Blueprint, request, redirect, render_template
from models import db, Book
books = Blueprint('books', __name__)
from werkzeug.utils import secure_filename


# ADD BOOK
@books.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    file = request.files.get('file')

    book = Book(title=title)

    if file and file.filename != "":
        filename = secure_filename(file.filename)

        # correct save path
        file.save(os.path.join('static', filename))

        # ONLY filename store
        book.file = filename

        print("DEBUG FILE:", filename)
    else:
        print("NO FILE RECEIVED ❌")

    db.session.add(book)
    db.session.commit()

    return redirect('/books')

# DELETE BOOK
@books.route('/delete_book/<int:id>')
def delete_book(id):
    book = db.session.get(Book, id)
    if book:
        db.session.delete(book)
        db.session.commit()

    return redirect('/books')


# EDIT BOOK
@books.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = db.session.get(Book, id)

    if request.method == 'POST':
        book.title = request.form['title']
        db.session.commit()
        return redirect('/books')

    return render_template('edit_book.html', book=book)


# BOOKS PAGE
@books.route('/books')
def books_page():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)