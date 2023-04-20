from flask import current_app
from app.extensions import db
from app.models.user import Blog_User
from app.models.posts import Blog_Posts
from app.models.themes import Blog_Theme
from app.models.comments import Blog_Comments, Blog_Replies
from app.models.stats import Blog_Stats
from app.models.bookmarks import Blog_Bookmarks
from app.models.likes import Blog_Likes
from app.models.contact import Blog_Contact
# from app.models.text import about_text_author, about_text_user  # dummie strings
from app.dummie_data import authors, posts, themes, comments
from app.account.helpers import hash_pw
from app.models.helpers import pic_src_user, pic_src_post, pic_src_theme, update_stats_comments_total, update_stats_users_total, update_likes, update_bookmarks, delete_comment, delete_reply, update_approved_post_stats, update_stats_users_active
from datetime import datetime


# Creating a super_admin, a default author account, and a default user account
# The super_admin is important as this will enable the management of all other users.
# The default author is created for the case of an author having his/her account deleted: the posts
# created by this user will be passed onto the default author's account, to avoid loss of online content.
# The default user is created to avoid the loss of comments when a user's account it deleted: it will 'gain ownership' of deleted comments to prevent mismatch in treads.
# you can re-define the log-in credentials for these users by changing the variables bellow.
ADMIN_NAME = "Super Admin"
ADMIN_EMAIL = "super@admin"
ADMIN_PW = "admin123"
ADMIN_PICTURE = "Picture_default.jpg"
DEFAULT_AUTHOR_NAME = "The Travel Blog Team"
DEFAULT_AUTHOR_EMAIL = "travel@team"
DEFAULT_AUTHOR_PW = "author123"
DEFAULT_AUTHOR_ABOUT = authors.authors_about
DEFAULT_AUTHOR_PICTURE = "Picture_default_author.jpg"
DEFAULT_USER_NAME = "[Deleted]"
DEFAULT_USER_EMAIL = "deleted@users"
DEFAULT_USER_PW = "user123"
DEFAULT_USER_ABOUT = "This user's account has been deleted"
DEFAULT_USER_PICTURE = "Picture_default.jpg"

def create_admin_acct():
    # Check if a super_admin exists in the database, if not, add it as well as the default author and default user:
    # Note that these three users will not count towards the number of users using the blog (in the blog stats)
    super_admin_exists = Blog_User.query.get(1)
    if not super_admin_exists:
        the_super_admin = Blog_User(
            name=ADMIN_NAME, email=ADMIN_EMAIL, password=hash_pw(ADMIN_PW), type="super_admin", picture=ADMIN_PICTURE)
        the_default_author = Blog_User(name=DEFAULT_AUTHOR_NAME, email=DEFAULT_AUTHOR_EMAIL, password=hash_pw(DEFAULT_AUTHOR_PW),
                                    type="author", about=DEFAULT_AUTHOR_ABOUT, picture=DEFAULT_AUTHOR_PICTURE)
        the_default_user = Blog_User(name=DEFAULT_USER_NAME, email=DEFAULT_USER_EMAIL, password=hash_pw(DEFAULT_USER_PW),
                                    type="user", about=DEFAULT_USER_ABOUT, picture=DEFAULT_USER_PICTURE)
        db.session.add(the_super_admin)
        db.session.add(the_default_author)
        db.session.add(the_default_user)
        db.session.commit()

# Creating the stats
def create_stats():
    # Check if stats table exists, if not, then add it:
    stats_exists = Blog_Stats.query.get(1)
    if not stats_exists:
        the_stats_table = Blog_Stats()
        db.session.add(the_stats_table)
        db.session.commit()

# Creating the themes
def create_themes():
    # Check if themes exist in the database, if not, add themes:
    dummies_exists = Blog_Theme.query.get(1)
    if not dummies_exists:
        theme1 = Blog_Theme(
            theme=themes.themes_data[0]["theme"], picture=themes.themes_data[0]["picture"], picture_source=themes.themes_data[0]["picture_source"])
        theme2 = Blog_Theme(
            theme=themes.themes_data[1]["theme"], picture=themes.themes_data[1]["picture"], picture_source=themes.themes_data[1]["picture_source"])
        theme3 = Blog_Theme(
            theme=themes.themes_data[2]["theme"], picture=themes.themes_data[2]["picture"], picture_source=themes.themes_data[2]["picture_source"])
        theme4 = Blog_Theme(
            theme=themes.themes_data[3]["theme"], picture=themes.themes_data[3]["picture"], picture_source=themes.themes_data[3]["picture_source"])

        db.session.add(theme1)
        db.session.add(theme2)
        db.session.add(theme3)
        db.session.add(theme4)
        db.session.commit()

# DUMMIE DATA
# Users, posts, comments, likes, and bookmarks were created for the purposes of testing and previewing the application
# These can be deleted. Plese note, however, that if you delete the posts without replacing them with new data, the blog may present a number of issues.
# Likewise, deleting the author's account created in this page without changing the authorship of the posts (or deleting the posts) will leave to issues.
# Dummie users are linked to data such as comments and likes. Deleting the creation of these without edditing or deleting their actions will result in  issues.

# Creating dummie user accounts: to test and use the app as example
# These users can be deleted without impacting the blog's usage
USER_PW = "user123"
USER_ABOUT = authors.authors_about

def create_dummie_accts():
    # Check if dummies exists in the database, if not, add dummie accounts:
    dummies_exists = Blog_User.query.get(4)
    if not dummies_exists:
        random1 = Blog_User(name="Roberta Sanstoms",
                            email="r@r", password=hash_pw(USER_PW), type="admin")
        random2 = Blog_User(name=authors.authors_data[0]["name"], email="e@e", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture=authors.authors_data[0]["picture"])
        random3 = Blog_User(name=authors.authors_data[1]["name"], email="j@j", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture=authors.authors_data[1]["picture"])
        random4 = Blog_User(name=authors.authors_data[2]["name"], email="m@m", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture=authors.authors_data[2]["picture"])
        random5 = Blog_User(name="John Meyers", email="j@m",
                            password=hash_pw(USER_PW), type="user")
        random6 = Blog_User(name="Fabienne123", email="f@f",
                            password=hash_pw(USER_PW), type="user")
        random7 = Blog_User(name="Kokaloka", email="k@k",
                            password=hash_pw(USER_PW), type="user")
        random8 = Blog_User(name="SublimePoster", email="s@p",
                            password=hash_pw(USER_PW), type="user")
        db.session.add(random1)
        db.session.add(random2)
        db.session.add(random3)
        db.session.add(random4)
        db.session.add(random5)
        db.session.add(random6)
        db.session.add(random7)
        db.session.add(random8)
        db.session.commit()
        for i in range(8):
            update_stats_users_total()
            update_stats_users_active(1)


# Creating dummie posts: to test and use the app as example
POST_INTRO = posts.post_intro
POST_BODY = posts.post_body
def create_posts():
    # Check if dummie posts exists in the database, if not, create the posts:
    posts_exist = Blog_Posts.query.get(1)
    if not posts_exist:
        post1 = Blog_Posts(theme_id = posts.post_data[0]["theme"], title = posts.post_data[0]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[0]["author_id"], picture_v=posts.post_data[0]["picture_v"], 
                            picture_v_source=posts.post_data[0]["picture_v_source"], picture_h=posts.post_data[0]["picture_h"],
                            picture_h_source=posts.post_data[0]["picture_h_source"], picture_s=posts.post_data[0]["picture_s"],
                            picture_s_source=posts.post_data[0]["picture_s_source"], picture_alt=posts.post_data[0]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[0]["date_submitted"], date_to_post=posts.post_data[0]["date_to_post"])
        post2 = Blog_Posts(theme_id = posts.post_data[1]["theme"], title = posts.post_data[1]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[1]["author_id"], picture_v=posts.post_data[1]["picture_v"], 
                            picture_v_source=posts.post_data[1]["picture_v_source"], picture_h=posts.post_data[1]["picture_h"],
                            picture_h_source=posts.post_data[1]["picture_h_source"], picture_s=posts.post_data[1]["picture_s"],
                            picture_s_source=posts.post_data[1]["picture_s_source"], picture_alt=posts.post_data[1]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[1]["date_submitted"], date_to_post=posts.post_data[1]["date_to_post"])
        post3 = Blog_Posts(theme_id = posts.post_data[2]["theme"], title = posts.post_data[2]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[2]["author_id"], picture_v=posts.post_data[2]["picture_v"], 
                            picture_v_source=posts.post_data[2]["picture_v_source"], picture_h=posts.post_data[2]["picture_h"],
                            picture_h_source=posts.post_data[2]["picture_h_source"], picture_s=posts.post_data[2]["picture_s"],
                            picture_s_source=posts.post_data[2]["picture_s_source"], picture_alt=posts.post_data[2]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[2]["date_submitted"], date_to_post=posts.post_data[2]["date_to_post"])
        post4 = Blog_Posts(theme_id = posts.post_data[3]["theme"], title = posts.post_data[3]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[3]["author_id"], picture_v=posts.post_data[3]["picture_v"], 
                            picture_v_source=posts.post_data[3]["picture_v_source"], picture_h=posts.post_data[3]["picture_h"],
                            picture_h_source=posts.post_data[3]["picture_h_source"], picture_s=posts.post_data[3]["picture_s"],
                            picture_s_source=posts.post_data[3]["picture_s_source"], picture_alt=posts.post_data[3]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[3]["date_submitted"], date_to_post=posts.post_data[3]["date_to_post"])
        post5 = Blog_Posts(theme_id = posts.post_data[4]["theme"], title = posts.post_data[4]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[4]["author_id"], picture_v=posts.post_data[4]["picture_v"], 
                            picture_v_source=posts.post_data[4]["picture_v_source"], picture_h=posts.post_data[4]["picture_h"],
                            picture_h_source=posts.post_data[4]["picture_h_source"], picture_s=posts.post_data[4]["picture_s"],
                            picture_s_source=posts.post_data[4]["picture_s_source"], picture_alt=posts.post_data[4]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[4]["date_submitted"], date_to_post=posts.post_data[4]["date_to_post"])
        post6 = Blog_Posts(theme_id = posts.post_data[5]["theme"], title = posts.post_data[5]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[5]["author_id"], picture_v=posts.post_data[5]["picture_v"], 
                            picture_v_source=posts.post_data[5]["picture_v_source"], picture_h=posts.post_data[5]["picture_h"],
                            picture_h_source=posts.post_data[5]["picture_h_source"], picture_s=posts.post_data[5]["picture_s"],
                            picture_s_source=posts.post_data[5]["picture_s_source"], picture_alt=posts.post_data[5]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[5]["date_submitted"], date_to_post=posts.post_data[5]["date_to_post"])
        post7 = Blog_Posts(theme_id = posts.post_data[6]["theme"], title = posts.post_data[6]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[6]["author_id"], picture_v=posts.post_data[6]["picture_v"], 
                            picture_v_source=posts.post_data[6]["picture_v_source"], picture_h=posts.post_data[6]["picture_h"],
                            picture_h_source=posts.post_data[6]["picture_h_source"], picture_s=posts.post_data[6]["picture_s"],
                            picture_s_source=posts.post_data[6]["picture_s_source"], picture_alt=posts.post_data[6]["picture_alt"],
                            admin_approved= "TRUE", date_submitted=posts.post_data[6]["date_submitted"], date_to_post=posts.post_data[6]["date_to_post"])
        post8 = Blog_Posts(theme_id = posts.post_data[7]["theme"], title = posts.post_data[7]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[7]["author_id"], picture_v=posts.post_data[7]["picture_v"], 
                            picture_v_source=posts.post_data[7]["picture_v_source"], picture_h=posts.post_data[7]["picture_h"],
                            picture_h_source=posts.post_data[7]["picture_h_source"], picture_s=posts.post_data[7]["picture_s"],
                            picture_s_source=posts.post_data[7]["picture_s_source"], picture_alt=posts.post_data[7]["picture_alt"],
                            admin_approved= "TRUE", date_submitted=posts.post_data[7]["date_submitted"], date_to_post=posts.post_data[7]["date_to_post"])
        post9 = Blog_Posts(theme_id = posts.post_data[8]["theme"], title = posts.post_data[8]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[8]["author_id"], picture_v=posts.post_data[8]["picture_v"], 
                            picture_v_source=posts.post_data[8]["picture_v_source"], picture_h=posts.post_data[8]["picture_h"],
                            picture_h_source=posts.post_data[8]["picture_h_source"], picture_s=posts.post_data[8]["picture_s"],
                            picture_s_source=posts.post_data[8]["picture_s_source"], picture_alt=posts.post_data[8]["picture_alt"],
                            admin_approved= "TRUE", date_submitted=posts.post_data[8]["date_submitted"], date_to_post=posts.post_data[8]["date_to_post"])
        post10 = Blog_Posts(theme_id = posts.post_data[9]["theme"], title = posts.post_data[9]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[9]["author_id"], picture_v=posts.post_data[9]["picture_v"], 
                            picture_v_source=posts.post_data[9]["picture_v_source"], picture_h=posts.post_data[9]["picture_h"],
                            picture_h_source=posts.post_data[9]["picture_h_source"], picture_s=posts.post_data[9]["picture_s"],
                            picture_s_source=posts.post_data[9]["picture_s_source"], picture_alt=posts.post_data[9]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[9]["date_submitted"], date_to_post=posts.post_data[9]["date_to_post"])
        post11 = Blog_Posts(theme_id=posts.post_data[10]["theme"], title=posts.post_data[10]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[10]["author_id"], picture_v=posts.post_data[10]["picture_v"],
                            picture_v_source=posts.post_data[10]["picture_v_source"], picture_h=posts.post_data[10]["picture_h"],
                            picture_h_source=posts.post_data[10]["picture_h_source"], picture_s=posts.post_data[10]["picture_s"],
                            picture_s_source=posts.post_data[10]["picture_s_source"], picture_alt=posts.post_data[10]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[10]["date_submitted"], date_to_post=posts.post_data[10]["date_to_post"])
        post12 = Blog_Posts(theme_id=posts.post_data[11]["theme"], title=posts.post_data[11]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[11]["author_id"], picture_v=posts.post_data[11]["picture_v"],
                            picture_v_source=posts.post_data[11]["picture_v_source"], picture_h=posts.post_data[11]["picture_h"],
                            picture_h_source=posts.post_data[11]["picture_h_source"], picture_s=posts.post_data[11]["picture_s"],
                            picture_s_source=posts.post_data[11]["picture_s_source"], picture_alt=posts.post_data[11]["picture_alt"],
                            admin_approved="TRUE", date_submitted=posts.post_data[11]["date_submitted"], date_to_post=posts.post_data[11]["date_to_post"])
        post13 = Blog_Posts(theme_id=posts.post_data[12]["theme"], title=posts.post_data[12]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[12]["author_id"], picture_v=posts.post_data[12]["picture_v"],
                            picture_v_source=posts.post_data[12]["picture_v_source"], picture_h=posts.post_data[12]["picture_h"],
                            picture_h_source=posts.post_data[12]["picture_h_source"], picture_s=posts.post_data[12]["picture_s"],
                            picture_s_source=posts.post_data[12]["picture_s_source"], picture_alt=posts.post_data[12]["picture_alt"])
        post14 = Blog_Posts(theme_id=posts.post_data[13]["theme"], title=posts.post_data[13]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[13]["author_id"], picture_v=posts.post_data[13]["picture_v"],
                            picture_v_source=posts.post_data[13]["picture_v_source"], picture_h=posts.post_data[13]["picture_h"],
                            picture_h_source=posts.post_data[13]["picture_h_source"], picture_s=posts.post_data[13]["picture_s"],
                            picture_s_source=posts.post_data[13]["picture_s_source"], picture_alt=posts.post_data[13]["picture_alt"])
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.add(post4)
        db.session.add(post5)
        db.session.add(post6)
        db.session.add(post7)
        db.session.add(post8)
        db.session.add(post9)
        db.session.add(post10)
        db.session.add(post11)
        db.session.add(post12)
        db.session.add(post13)
        db.session.add(post14)
        db.session.commit()

        for i in range (12):
            update_approved_post_stats(1)

# Creating dummie comments in posts

def create_comments():
    comments_exist = Blog_Comments.query.get(1)
    if not comments_exist:
        comment1 = Blog_Comments(text=comments.comment_data[0]["text"], post_id=1, user_id=4)
        comment2 = Blog_Comments(text=comments.comment_data[1]["text"], post_id=2, user_id=4)
        comment3 = Blog_Comments(text=comments.comment_data[2]["text"], post_id=2, user_id=4, date_submitted=datetime.strptime("2023-02-01 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment4 = Blog_Comments(text=comments.comment_data[3]["text"], post_id=2, user_id=4, blocked="TRUE")
        comment5 = Blog_Replies(text=comments.comment_data[4]["text"], post_id=2, user_id=5, comment_id=3, date_submitted=datetime.strptime("2023-02-02 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment6 = Blog_Replies(text=comments.comment_data[5]["text"], post_id=2, user_id=4, comment_id=3, date_submitted=datetime.strptime("2023-02-03 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment7 = Blog_Replies(text=comments.comment_data[6]["text"], post_id=2, user_id=5, comment_id=3, date_submitted=datetime.strptime("2023-02-04 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment8 = Blog_Replies(text=comments.comment_data[7]["text"], post_id=2, user_id=5, comment_id=3, blocked="TRUE", date_submitted=datetime.strptime("2023-02-05 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment9 = Blog_Comments(text=comments.comment_data[3]["text"], post_id=3, user_id=6)
        comment10 = Blog_Replies(text=comments.comment_data[7]["text"], post_id=3, user_id=5, comment_id=5)
        db.session.add(comment1)
        db.session.add(comment2)
        db.session.add(comment3)
        db.session.add(comment4)
        db.session.add(comment5)
        db.session.add(comment6)
        db.session.add(comment7)
        db.session.add(comment8)
        db.session.add(comment9)
        db.session.add(comment10)
        db.session.commit()

        for i in range(10):
            update_stats_comments_total()

# Create dummie Likes and Bookmarks in the database, as well as updating the 'stats' related to those
def create_likes_and_bookmarks():
    likes_exist = Blog_Likes.query.get(1)
    if not likes_exist:
        like1 = Blog_Likes(post_id=2, user_id=4)
        like2 = Blog_Likes(post_id=2, user_id=5)
        like3 = Blog_Likes(post_id=2, user_id=6)
        like4 = Blog_Likes(post_id=2, user_id=7)
        like5 = Blog_Likes(post_id=1, user_id=7)
        like6 = Blog_Likes(post_id=3, user_id=6)
        like7 = Blog_Likes(post_id=3, user_id=8)
        like8 = Blog_Likes(post_id=4, user_id=8)
        like9 = Blog_Likes(post_id=5, user_id=8)
        like10 = Blog_Likes(post_id=6, user_id=4)
        bookmark1 = Blog_Bookmarks(post_id=2, user_id=4)
        bookmark2 = Blog_Bookmarks(post_id=1, user_id=4)
        bookmark3 = Blog_Bookmarks(post_id=4, user_id=5)
        bookmark4 = Blog_Bookmarks(post_id=6, user_id=5)
        bookmark5 = Blog_Bookmarks(post_id=2, user_id=5)
        bookmark6 = Blog_Bookmarks(post_id=1, user_id=6)
        bookmark7 = Blog_Bookmarks(post_id=3, user_id=6)
        bookmark8 = Blog_Bookmarks(post_id=4, user_id=6)
        bookmark9 = Blog_Bookmarks(post_id=5, user_id=7)
        bookmark10 = Blog_Bookmarks(post_id=6, user_id=7)
        db.session.add(like1)
        db.session.add(like2)
        db.session.add(like3)
        db.session.add(like4)
        db.session.add(like5)
        db.session.add(like6)
        db.session.add(like7)
        db.session.add(like8)
        db.session.add(like9)
        db.session.add(like10)
        db.session.add(bookmark1)
        db.session.add(bookmark2)
        db.session.add(bookmark3)
        db.session.add(bookmark4)
        db.session.add(bookmark5)
        db.session.add(bookmark6)
        db.session.add(bookmark7)
        db.session.add(bookmark8)
        db.session.add(bookmark9)
        db.session.add(bookmark10)
        db.session.commit()
        for i in range (10):
            update_likes(1)
            update_bookmarks(1)

# Testing the contact model:
def create_contact_db():
    contacts_exist = Blog_Contact.query.get(1)
    if not contacts_exist:
        new_contact = Blog_Contact(
            name="test", email="test", message="test")
        db.session.add(new_contact)
        db.session.commit()
