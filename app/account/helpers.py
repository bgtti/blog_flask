from flask import current_app
from werkzeug.security import generate_password_hash  # used in signup

# helper function to hash and salt password
def hash_pw(password):
    return generate_password_hash(
        password,
        method="pbkdf2:sha256",
        salt_length=8
    )

