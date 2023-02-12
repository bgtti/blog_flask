from app.extensions import db
from datetime import datetime

# note the Blog_Posts class has two fields: all_likes and likes
# likes are used to track registered user's posts likes, while all_likes registers the likes from non-registed users as well.
# the latter is tracked with the use of cookies.
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
    featured = db.Column(db.String(5), default="FALSE")
    # all_likes = db.Column(db.Integer, default=0)
    likes = db.relationship('Blog_Likes', backref='post')
    comments = db.relationship('Blog_Comments', backref='target_post')
    replies = db.relationship('Blog_Replies', backref='target_post')
    bookmarks = db.relationship('Blog_Bookmarks', backref='post')
    author_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))
    theme_id = db.Column(db.Integer, db.ForeignKey('blog_theme.id'))
    
    def __repr__(self):
        return f"<Post {self.id}: {self.title}, Theme: {self.theme_id}>"
