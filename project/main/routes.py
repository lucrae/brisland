from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from secrets import token_hex
from project.models import db, User, Post
from project.forms import EnterForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index(): # log in with just password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = EnterForm(request.form)

    # ip_address = request.environ.get('HTTP_X_REAL_IP') or request.environ.get('REMOTE_ADDR')
    ip_address = None

    # search for existent user
    user = User.query.filter_by(ip_address=ip_address).first()
    if user is None or ip_address is None:
        new_user = True
        usertag = token_hex(2)
    else:
        new_user = False
        usertag = user.tag

    if request.method == 'POST':

        if new_user: # create new user if need be
            user = User(ip_address, tag=usertag)
            db.session.add(user)
            db.session.commit()
    
        login_user(user, remember=True) # login

        return redirect(url_for('main.home'))

    return render_template("index.html", form=form, usertag=usertag)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/home')
@login_required
def home():
    posts = list(reversed(Post.query.all()))
    return render_template("home.html", posts=posts)