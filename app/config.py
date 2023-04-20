import os
from dotenv import load_dotenv  # getting .env variables
from datetime import timedelta

class Config:
    SECRET_KEY = "myFlaskApp4Fun"  # needed for login with wtforms
    SQLALCHEMY_DATABASE_URI = 'sqlite:///admin.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    ABSOLUTE_PATH = os.path.dirname(__file__)
    RELATIVE_PATH = "static/Pictures_Users"
    BLOG_PICTURES_PATH = "static/Pictures_Posts"
    PROFILE_IMG_FOLDER = os.path.join(ABSOLUTE_PATH, RELATIVE_PATH)
    BLOG_IMG_FOLDER = os.path.join(ABSOLUTE_PATH, BLOG_PICTURES_PATH)
    STATIC_FOLDER = os.path.join(ABSOLUTE_PATH, "static")
    ALLOWED_IMG_EXTENSIONS = ['PNG', 'JPG', 'JPEG']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

