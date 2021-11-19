from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from flask_login import current_user, login_required
from . import db
from .models import Book, User

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user= current_user)

