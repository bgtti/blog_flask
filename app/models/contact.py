from app.extensions import db
from datetime import datetime

class Blog_Contact(db.Model):
    __tablename__ = "blog_contact"
    # __bind_key__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(700))
