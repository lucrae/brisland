import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(4), default=secrets.token_hex(2), unique=True)
    ip_address = db.Column(db.String(64))
    password = db.Column(db.String(64), default=None)

    def __init__(self, ip_address, tag=secrets.token_hex(2), password=None):
        self.ip_address = ip_address
        self.tag = tag
        self.password = password

    def __repr__(self):
        return '<User({}, {})>'.format(self.id, self.tag)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(4), default=secrets.token_hex(2), unique=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), default=1)
    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
    board = db.relationship('Board', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, body, user_id, board_id=1):
        self.body = body
        self.user_id = user_id
        self.board_id = board_id

    def __repr__(self):
        return '<Post({}, {}, {}, {})>'.format(self.id, self.tag, self.user_id, self.board_id)

    @property
    def relative_timestamp(self):
        diff = datetime.utcnow() - self.timestamp
        s = int(diff.seconds)
        if diff.days > 7 or diff.days < 0: return d.strftime('%d %b %y')
        elif diff.days == 1: return '1 day ago'
        elif diff.days > 1: return '{} days ago'.format(diff.days)
        elif s <= 1: return 'just now'
        elif s < 60: return '{} seconds ago'.format(s)
        elif s < 120: return '1 minute ago'
        elif s < 3600: return '{} minutes ago'.format(s//60)
        elif s < 7200: return '1 hour ago'
        else: return '{} hours ago'.format(s//3600)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suffix = db.Column(db.String(8))
    icon = db.Column(db.String(16), default='globe')

    def __init__(self, suffix, icon):
        self.suffix = suffix
        self.icon = icon

    def __repr__(self):
        return '<Board({}, {})>'.format(self.id, self.suffix)