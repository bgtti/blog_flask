from app.models.stats import Blog_Stats
from app.extensions import db

# Functions that take the picture's name and output the path to the source file
def pic_src_post(picture_name):
    return f"../static/Pictures_Posts/{picture_name}"

def pic_src_theme(picture_name):
    return f"../static/Pictures_Themes/{picture_name}"

def pic_src_user(picture_name):
    return f"../static/Pictures_Users/{picture_name}"

# Functions that update the statistics (Stats)
def update_stats_comments_total():
    stats = Blog_Stats.query.get_or_404(1)
    modify_stats = int(stats.comments_total) + 1
    stats.comments_total = modify_stats
    db.session.commit()

# note that default users will not be added to the stats
def update_stats_users_total():
    stats = Blog_Stats.query.get_or_404(1)
    modify_stats = int(stats.user_total) + 1
    stats.user_total = modify_stats
    db.session.commit()

