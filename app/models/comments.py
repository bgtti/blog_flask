from app.extensions import db
from datetime import datetime


class Blog_Comments(db.Model):
    __tablename__ = "blog_comments"
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.String(500), nullable=False)
    blocked = db.Column(db.String(5), default="FALSE")  # TRUE or FALSE
    if_blocked = db.Column(
        db.String(100), default="[removed]")  # if blocked, show this text
    replies = db.relationship('Blog_Replies', backref='comment')
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))

    def __repr__(self):
        return f"<Comment {self.id}: {self.text}>"


class Blog_Replies(db.Model):
    __tablename__ = "blog_replies"
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.String(500), nullable=False)
    blocked = db.Column(db.String(5), default="FALSE")  # TRUE or FALSE
    if_blocked = db.Column(
        db.String(100), default="[removed]")  # if blocked, show this text
    likes = db.Column(db.Integer, default=0)
    comment_id = db.Column(db.Integer, db.ForeignKey('blog_comments.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))

    def __repr__(self):
        return f"<Reply {self.id}: {self.text}>"
