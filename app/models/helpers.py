# Functions that take the picture's name and output the path to the source file

def pic_src_post(picture_name):
    return f"../static/Pictures_Posts/{picture_name}"

def pic_src_theme(picture_name):
    return f"../static/Pictures_Themes/{picture_name}"

def pic_src_author(picture_name):
    return f"../static/Pictures_Users/{picture_name}"
