from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()
image = db.Column(db.String(300))
file = db.Column(db.String(300))  
image = db.Column(db.String(200))


# USER TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# BOOK TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    available = db.Column(db.Boolean, default=True)
    file = db.Column(db.String(200))
    

# ISSUE TABLE (IMPORTANT)
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #  FOREIGN KEYS (MOST IMPORTANT)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)

    #  RELATIONSHIP
    user = db.relationship('User', backref='issued_books')
    book = db.relationship('Book', backref='issued_books')


# 📌 REQUEST TABLE (NEW)
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_name = db.Column(db.String(200))
    status = db.Column(db.String(50), default="Pending")

    user = db.relationship('User', backref='requests')

# EBOOK TABLE
class ebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    file = db.Column(db.String(200))

# EBOOK-ISSUE TABLE
class ebook_issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'))

    issue_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)

    user = db.relationship('User', backref='issued_ebooks')
    ebook = db.relationship('ebook', backref='issued_ebooks')