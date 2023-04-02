from flask import Blueprint, render_template

error_handler = Blueprint('error_handler', __name__)

# 404 and 500 Errors

@error_handler.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@error_handler.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
