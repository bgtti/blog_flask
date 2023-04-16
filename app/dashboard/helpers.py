from app.general_helpers.helpers import check_image_filename
from werkzeug.utils import secure_filename
from flask import current_app
import os

def check_blog_picture(post_id, filename, db_column):
    """
    This function checks whether a picture uploaded to a blog post has the right file extension and gives the picture a new name.
    If the file extension is not supported, it returns 'False'
    Arguments: the post's id, the filename, and the database column where it should be added: "v", "h", or "s".
    Import the secure_filename function from werkzeug.utils and use it to supply the required filename argument.
    """
    
    # Check supplied arguments
    if db_column == "v" or db_column == "h" or db_column == "s":
        if type(post_id) is not int:
            return False
        if not check_image_filename(filename):
            return False
        
        # return new filename:
        post_id_str = str(post_id)
        extension = filename.rsplit(".", 1)[1]
        pic_new_name = "Picture_" + db_column + "_" + post_id_str + "." + extension
        return pic_new_name
    else:
        return False


def delete_blog_img(img):
        """Accepts blog image name and deletes it from folder or raises name error."""
        if img != None and os.path.exists(os.path.join(current_app.config["BLOG_IMG_FOLDER"], img)):
            try:
                os.remove(os.path.join(current_app.config["BLOG_IMG_FOLDER"], img))
            except:
                raise NameError("Blog post image could not be deleted.")
