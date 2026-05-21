from flask import Blueprint, render_template, session, redirect, request
from models import db, ebook
from werkzeug.utils import secure_filename
import os

ebook_bp = Blueprint('ebook_bp', __name__)

# PAGE
@ebook_bp.route('/ebooks')
def ebooks():
    if 'user' not in session:
        return redirect('/')

    books = ebook.query.all()
    return render_template('ebooks.html', books=books, user=session['user'])


# ADD
@ebook_bp.route('/add_ebook', methods=['POST'])
def add_ebook():
    title = request.form['title']
    file = request.files.get('file')

    ebook_obj = ebook(title=title)

    if file and file.filename:
        filename = secure_filename(file.filename)

        if not filename.lower().endswith('.pdf'):
            return "Only PDF allowed ❌"

        file.save(os.path.join('static', filename))
        ebook_obj.file = filename

    db.session.add(ebook_obj)
    db.session.commit()

    return redirect('/ebooks')


# DELETE
@ebook_bp.route('/delete_ebook/<int:id>')
def delete_ebook(id):
    ebook_obj = db.session.get(ebook, id)

    if ebook_obj:
        db.session.delete(ebook_obj)
        db.session.commit()

    return redirect('/ebooks')


# EDIT
@ebook_bp.route('/edit_ebook/<int:id>', methods=['GET', 'POST'])
def edit_ebook(id):
    ebook_obj = db.session.get(ebook, id)

    if request.method == 'POST':
        ebook_obj.title = request.form['title']
        db.session.commit()
        return redirect('/ebooks')

    return render_template('edit_ebook.html', book=ebook_obj)