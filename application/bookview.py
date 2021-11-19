from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from . import db
from .models import Book, User
from flask_paginate import Pagination, get_page_parameter
import sqlite3 as sql
import requests

bookview = Blueprint('bookview', __name__)

@bookview.route('/addbook', methods= ["GET", "POST"])
@login_required
def addbook():
    if request.method == "POST":
        isbn = request.form.get("isbn").strip()
        specialNotes = request.form.get("specialNotes")
        bookType = request.form.get("bookType")
        print(type(isbn))
        books = requests.get("https://www.googleapis.com/books/v1/volumes?q=%20+isbn:" + isbn + "&key=AIzaSyAFjocizDpIwD5jECWtNaRWMoz1dKSv4kQ").json()
        for book in books["items"]:
            bookName = book["volumeInfo"]["title"]
            Author = book["volumeInfo"]["authors"] 
            bookAuthor = ",".join(Author)
            bookDescription = book["volumeInfo"]["description"]
            thumbnail = book["volumeInfo"]["imageLinks"]["thumbnail"]

        book = Book.query.filter_by(isbn=isbn).filter_by(user_id=current_user.id).first()

        if book :
            flash("Book Already added.", category="error")
        elif not (len(isbn) == 13 or 10):
            flash("please enter valid ISBN", category="error")
        else:
            new_book = Book(bookName = bookName, bookAuthor = bookAuthor, bookDescription= bookDescription, bookType= bookType, specialNotes= specialNotes, thumbnail=thumbnail , isbn= isbn ,user_id= current_user.id)
            db.session.add(new_book)
            db.session.commit()
            flash("Book added Successfully", category="success")
            return render_template('addbook.html', user= current_user)

    return render_template('addbook.html', user= current_user)

@bookview.route("/mybooks", methods= ["GET", "POST"])
@login_required
def mybooks():
    page= request.args.get('page', 1, type=int)
    books = Book.query.filter_by(user_id= current_user.id).paginate(page=page, per_page=5)

    
    return render_template("mybooks.html", user= current_user, books= books)


@bookview.route("/delete/<int:id>", methods= ["GET", "POST"])
@login_required
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully", category="success")
    return redirect(url_for('bookview.mybooks'))

@bookview.route("/edit/<int:id>", methods= ["GET", "POST"])
@login_required
def edit_book(id):
    book_existing = Book.query.filter_by(id=id).first()
    if request.method=="POST":

        specialNotes = request.form.get("specialNotes")
        bookType = request.form.get("bookType")
        new_book = Book(bookName = book_existing.bookName, bookAuthor = book_existing.bookAuthor, bookDescription= book_existing.bookDescription, bookType= bookType, isbn= book_existing.isbn, specialNotes= specialNotes, thumbnail= book_existing.thumbnail ,user_id= current_user.id)
        db.session.delete(book_existing)
        db.session.add(new_book)
        db.session.commit()

        flash("Changes saved successfully", category="success")
        return redirect(url_for("bookview.mybooks"))

    return render_template("edit.html", user=current_user)

# @bookview.route("/search", methods= ["GET", "POST"])
# @login_required
# def search():
#     if request.method == "POST":
#         if request.form.get("search"):
#             search = request.form.get("search")
#             books = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + search +"&key=AIzaSyAFjocizDpIwD5jECWtNaRWMoz1dKSv4kQ").json()
#         # book= books.items()
#             for book in books["items"]:
#                 print(book["volumeInfo"]["title"])
#             # print(books)

#         # books = "searchResults.html", books = requests.get("https://www.googleapis.com/books/v1/volumes?q=" +
#                             #    request.form.get("title") + "+inauthor:" + request.form.get("author") +
#                             #    "&key=AIzaSyBtprivgL2dXOf8kxsMHuELzvOAQn-2ZZM").json())
#             return render_template("searchresult.html",user=current_user, books = books)
    
#     return render_template("search.html", user= current_user)

