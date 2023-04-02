import os
from dotenv import load_dotenv  # getting .env variables
from datetime import timedelta

class Config:
    # needed for login with wtforms
    SECRET_KEY = "myFlaskApp4Fun"  # needed for login with wtforms
    SQLALCHEMY_DATABASE_URI = 'sqlite:///admin.db'  # can use: 'sqlite:///admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    # PERMANENT_SESSION_LIFETIME = timedelta(days=5)
    ABSOLUTE_PATH = os.path.dirname(__file__)
    RELATIVE_PATH = "static/Pictures_Users"
    PROFILE_IMG_FOLDER = os.path.join(ABSOLUTE_PATH, RELATIVE_PATH)
    STATIC_FOLDER = os.path.join(ABSOLUTE_PATH, "static")
    ALLOWED_IMG_EXTENSIONS = ['PNG', 'JPG', 'JPEG']
    # STATIC_URL_PATH = "../static"
    # STATIC_FOLDER = "../static"
