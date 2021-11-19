from enum import unique
from  . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bookName = db.Column(db.String(150))
    bookAuthor = db.Column(db.String(150))
    bookDescription = db.Column(db.String(1000))
    bookType = db.Column(db.String(20))
    isbn = db.Column(db.Integer)
    thumbnail = db.Column(db.String(250))
    specialNotes = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique= True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    books = db.relationship('Book')