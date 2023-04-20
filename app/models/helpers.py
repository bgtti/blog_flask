from app.models.stats import Blog_Stats
from app.models.comments import Blog_Comments, Blog_Replies
from app.models.posts import Blog_Posts
from app.extensions import db
from sqlalchemy import desc

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
    """
    Counts number of users who created an account. Does not take into acount users who deleted their accounts.
    This function updates the blog statistics database.
    """
    stats = Blog_Stats.query.get_or_404(1)
    modify_stats = int(stats.user_total) + 1
    stats.user_total = modify_stats
    db.session.commit()
    
# note that default users will not be added to the stats
def update_stats_users_active(num):
    """
    Takes -1 or 1 as arguments. 1 when a user creates an account, -1 when a user deletes an account.
    This function updates the blog statistics database.
    """
    if num == -1 or num == 1:
        stats = Blog_Stats.query.get_or_404(1)
        if num == 1:
            modify_stats = int(stats.user_active_total) + 1
            stats.user_active_total = modify_stats
        else:
            modify_stats = int(stats.user_active_total) - 1
            stats.user_active_total = modify_stats
        db.session.commit()
    else:
        return print("Invalid arguments given to def update_stats_users_active function.")

# takes -1 or 1 as arguments: whether user likes or un-likes a post
def update_likes(num):
    """
    Takes -1 or 1 as arguments. -1 if user un-likes a post, and 1 if user likes a post.
    This function updates the blog statistics database.
    """
    if num == -1 or num == 1:
        stats = Blog_Stats.query.get_or_404(1)
        if num == 1:
            modify_stats = int(stats.likes_total) + 1
            stats.likes_total = modify_stats
        else:
            modify_stats = int(stats.likes_total) - 1
            stats.likes_total = modify_stats
            
        db.session.commit()
    else:
        return print("Invalid arguments given to def update_likes function.")

# takes -1 or 1 as arguments: whether user bookmarks or un-bookmarks a post
def update_bookmarks(num):
    """
    Takes -1 or 1 as arguments. -1 if user un-bookmarks a post, and 1 if user bookmarks a post.
    This function updates the blog statistics database.
    """
    if num == -1 or num == 1:
        stats = Blog_Stats.query.get_or_404(1)
        if num == 1:
            modify_stats = int(stats.bookmarks_total) + 1
            stats.bookmarks_total = modify_stats
        else:
            modify_stats = int(stats.bookmarks_total) - 1
            stats.bookmarks_total = modify_stats
        db.session.commit()
    else:
        return print("Invalid arguments given to update_bookmarks function.")
    
# takes -1 or 1 as arguments: whether post is approved (1) or disapproved (-1). If a post is approved, then deleted = -1. If a post is deleted but was never approved, do not use this function.
def update_approved_post_stats(num):
    """
    Takes -1 or 1 as arguments. Only to be used on approved posts. -1 if a post is disapproved, 1 when a post is approved.
    If a post was approved, but it then deleted, -1.
    This function updates the blog statistics database.
    """
    if num == -1 or num == 1:
        stats = Blog_Stats.query.get_or_404(1)
        if num == 1:
            modify_stats = int(stats.posts_approved) + 1
            stats.posts_approved = modify_stats
        else:
            modify_stats = int(stats.posts_approved) - 1
            stats.posts_approved = modify_stats
        db.session.commit()
    else:
        return print("Invalid arguments given to update_approved_post_stats function.")

# deleting a comment
# comments which have replies will be blocked instead of deleted.
# they will present information as [deleted]
def delete_comment(commentId):
    """
    Takes comment ID as an argument, which must be an int.
    Returns "success" or "404" if comment is not found.
    If comment has replies, it will be blocked. If it does not, it will be deleted.
    """
    # check if ID is int
    if not isinstance(commentId, int):
        raise Exception("The id should be an integer")
    # check if comment exists:
    the_comment = Blog_Comments.query.get(commentId)
    if the_comment:
        replies = db.session.query(Blog_Replies).filter(
            Blog_Replies.comment_id == commentId).first()
        if replies:
            the_comment.blocked = "TRUE"
            the_comment.if_blocked = "[deleted]"
            db.session.commit()
        else:
            db.session.delete(the_comment)
            db.session.commit()
        return "success"
    else:
        print("You had an issue with the delete_comment function.")
        return 404

# if blog comment does not have other replies, reply will be deleted.
# if comment has many replies, it will only be deleted if it is the latest reply
def delete_reply(replyId):
    """
    Takes replyId as an argument, which must be an int.
    Returns "success" or "404" if comment is not found.
    Replies which are not the latest reply will be blocked instead of deleted.
    """
    # logic here
    # check if ID is int
    if not isinstance(replyId, int):
        raise Exception("The id should be an integer")
    # check if reply exists:
    the_reply = Blog_Replies.query.get(replyId)
    if (the_reply):
        # see if there are more replies to the comment
        the_comment = Blog_Comments.query.get(the_reply.comment_id)
        if not the_comment:
            return 404
        # get last 2 comments
        all_replies = [[r.id, r.date_submitted] for r in db.session.query(Blog_Replies).filter(
            Blog_Replies.comment_id == the_comment.id,).order_by(desc(Blog_Replies.date_submitted)).limit(2)]
        # if reply is the latest comment, delete, if not, block
        if all_replies[0][0] == replyId:
            db.session.delete(the_reply)
            db.session.commit()
        else:
            the_reply.blocked = "TRUE"
            the_reply.if_blocked = "[deleted]"
            db.session.commit()
        return "success"
    else:
        print("You had an issue with the delete_reply function.")
        return 404

# Change the authorship of all post
def change_authorship_of_all_post(current_author_id, new_author_id):
    """
    This function changes the authorship of all blog posts associated with an author.
    Arguments: current_author_id and new_author_id
    """
    all_posts_from_author = Blog_Posts.query.filter_by(
        author_id=current_author_id).all()

    for post in all_posts_from_author:
        post.author_id = new_author_id
    db.session.commit()
