from flask import Flask
import app.extensions as extensions
from app.config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # db = SQLAlchemy(app)
    extensions.db.init_app(app)
    extensions.ckeditor.init_app(app)
    extensions.login_manager.init_app(app)

    from app.account.routes import account
    from app.dashboard.routes import dashboard
    from app.website.routes import website
    from app.error_handlers.routes import error_handler
    from config import Config
    from flask import current_app

    from app.models import user, posts, themes, contact, bookmarks, comments, stats

    app.register_blueprint(account)
    app.register_blueprint(dashboard)
    app.register_blueprint(website)
    app.register_blueprint(error_handler)

    @app.route('/test/')
    def test_page():
        return '<h1> Testing the App </h1>'

    ABS_PATH = os.path.dirname(__file__)
    REL_PATH = "static"

    STATIC_PATH = repr(str(app.config["STATIC_FOLDER"]))
    
    @app.route("/../static/<filename>")
    def static_path():
        pass

    return app
