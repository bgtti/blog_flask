from app.extensions import db

class Blog_Theme(db.Model):
    __tablename__ = "blog_theme"
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(30), nullable=False)
    picture = db.Column(db.String(700), nullable=False)
    picture_source = db.Column(db.String(700))
    posts = db.relationship('Blog_Posts', backref='theme_group')

    def __repr__(self):
        return f"<Theme: {self.id} {self.theme}>"
