from flask import current_app

def check_image_filename(filename):
    """
    This function checks whether a picture has the right file extension.
    The function will return "True" if the file extension is correct or "False" if it is not.
    Argument: the filename is the only required argument.
    Import the secure_filename function from werkzeug.utils and use it to supply the required filename argument.
    """

    # Check the filename to see if extension is valid, and to check whether two extensions might be present (eg: .jpg.php)
    if not "." in filename:
        return False

    extension = filename.rsplit(".", 1)[1]

    if extension.upper() not in current_app.config["ALLOWED_IMG_EXTENSIONS"]:
        return False

    if filename.count('.') > 1:
        return False

    else:
        return True


