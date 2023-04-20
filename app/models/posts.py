from app.extensions import db
from datetime import datetime

class Blog_Posts(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    date_to_post = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    picture_v = db.Column(db.String(200))
    picture_v_source = db.Column(db.String(500))
    picture_h = db.Column(db.String(200))
    picture_h_source = db.Column(db.String(500))
    picture_s = db.Column(db.String(200))
    picture_s_source = db.Column(db.String(500))
    picture_alt = db.Column(db.String(200))
    meta_tag = db.Column(db.String(200))
    title_tag = db.Column(db.String(200))
    admin_approved = db.Column(db.String(5), default="FALSE")
    # featured is not being used at the moment, in the future can be used to 'feature' a post on a top modal, or similar
    featured = db.Column(db.String(5), default="FALSE")
    likes = db.relationship('Blog_Likes', backref='post')
    comments = db.relationship('Blog_Comments', backref='target_post')
    replies = db.relationship('Blog_Replies', backref='target_post')
    bookmarks = db.relationship('Blog_Bookmarks', backref='post')
    author_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))
    theme_id = db.Column(db.Integer, db.ForeignKey('blog_theme.id'))
    
    def __repr__(self):
        return f"<Post {self.id}: {self.title}, Theme: {self.theme_id}>"
