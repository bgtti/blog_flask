from app.extensions import db
from datetime import datetime


class Blog_Bookmarks(db.Model):
    __tablename__ = "blog_bookmarks"
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))

    def __repr__(self):
        return f"<Bookmarked>"
