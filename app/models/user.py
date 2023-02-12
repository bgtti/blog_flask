from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


class Blog_User(UserMixin, db.Model):
    __tablename__ = "blog_user"
    # __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    about = db.Column(db.String(385), default="")
    # in future, change picture to BLOB
    picture = db.Column(
        db.String(), default="../static/Pictures_Users/Picture_default.jpg")
    # type can be: admin, super_admin, author, or user
    type = db.Column(db.String(100), nullable=False, default="user")
    # comment = db.Column(db.String(700), default="")
    # whether user has been blocked (future implementation)
    blocked = db.Column(db.String(5), default="FALSE")
    # likes = db.Column(db.Integer, default=0)
    admin_notes = db.Column(db.Text)
    # posts = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    posts = db.relationship('Blog_Posts', backref='author')
    comments = db.relationship('Blog_Comments', backref='user')
    replies = db.relationship('Blog_Replies', backref='user')
    likes = db.relationship('Blog_Likes', backref='user')
    bookmarks = db.relationship('Blog_Bookmarks', backref='user')

    def __repr__(self):
        return f"<User: {self.id} {self.name} {self.email}>"
