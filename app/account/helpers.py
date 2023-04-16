from flask import current_app
from werkzeug.security import generate_password_hash  # used in signup
# helper function to hash and salt password
def hash_pw(password):
    return generate_password_hash(
        password,
        method="pbkdf2:sha256",
        salt_length=8
    )

#in general now:
# def allowed_imgs(filename):
#     if not "." in filename:
#         return False
#     extension = filename.rsplit(".", 1)[1]
#     if extension.upper() in current_app.config["ALLOWED_IMG_EXTENSIONS"]:
#         return True
#     else:
#         return False
