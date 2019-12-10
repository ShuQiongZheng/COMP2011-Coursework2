from app import db
from datetime import datetime
from flask_login import UserMixin

association_table = db.Table('association_table',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)

    user_name = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer)

    title = db.Column(db.String(40), nullable=False)

    description = db.Column(db.String(1024), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    like = db.Column(db.Integer, nullable=False, default=0)

    tag = db.relationship('Tag', secondary=association_table, backref='Book')

    def __init__(self,user_id,title,description,user_name):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.user_name = user_name

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password):  # 检查加密，调用werkzeug.security提供的方法
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

