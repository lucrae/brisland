from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from project.models import User, Post

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    users = User.query.all()
    posts = Post.query.all()

    return render_template("admin.html", users=users, posts=posts)
