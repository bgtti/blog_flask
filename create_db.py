from flask import current_app
from app.extensions import db
from app.models.user import Blog_User
from app.models.posts import Blog_Posts
from app.models.themes import Blog_Theme
from app.models.comments import Blog_Comments, Blog_Replies
from app.models.stats import Blog_Stats
from app.models.bookmarks import Blog_Bookmarks
from app.models.likes import Blog_Likes
# from app.models.text import about_text_author, about_text_user  # dummie strings
from app.dummie_data import authors, posts, themes
from app.account.helpers import hash_pw
from app.models.helpers import pic_src_user, pic_src_post, pic_src_theme, update_stats_comments_total, update_stats_users_total
from datetime import datetime


# Creating a super_admin and a default author account
# The super_admin is important as this will enable the management of all other users.
# The default author is created for the case of an author having his/her account deleted: the posts
# created by this user will be passed onto the default author's account, to avoid loss of online content.
# the default user will 'gain ownership' of deleted comments to prevent mismatch.
# you can re-define the log-in credentials for these users by changing the variables bellow.
ADMIN_PW = "admin123"
ADMIN_EMAIL = "super@admin"
ADMIN_NAME = "Super Admin"
ADMIN_PICTURE = "Picture_default.jpg"
DEFAULT_AUTHOR_PW = "author123"
DEFAULT_AUTHOR_EMAIL = "t@t"
DEFAULT_AUTHOR_NAME = "The Travel Blog Team"
DEFAULT_AUTHOR_ABOUT = authors.authors_about
DEFAULT_AUTHOR_PICTURE = "Picture_default_author.jpg"
DEFAULT_USER_PW = "user123"
DEFAULT_USER_EMAIL = "d@d"
DEFAULT_USER_NAME = "[Deleted]"
DEFAULT_USER_ABOUT = ""
DEFAULT_USER_PICTURE = "Picture_default.jpg"

def create_admin_acct():
    # Check if a super_admin exists in the database, if not, add it:
    super_admin_exists = Blog_User.query.get(1)
    if not super_admin_exists:
        the_super_admin = Blog_User(
            name=ADMIN_NAME, email=ADMIN_EMAIL, password=hash_pw(ADMIN_PW), type="super_admin", picture=pic_src_user(ADMIN_PICTURE))
        the_default_author = Blog_User(name=DEFAULT_AUTHOR_NAME, email=DEFAULT_AUTHOR_EMAIL, password=hash_pw(DEFAULT_AUTHOR_PW),
                                    type="author", about=DEFAULT_AUTHOR_ABOUT, picture=pic_src_user(DEFAULT_AUTHOR_PICTURE))
        the_default_user = Blog_User(name=DEFAULT_USER_NAME, email=DEFAULT_USER_EMAIL, password=hash_pw(DEFAULT_USER_PW),
                                    type="user", about=DEFAULT_USER_ABOUT, picture=pic_src_user(DEFAULT_USER_PICTURE))
        db.session.add(the_super_admin)
        db.session.add(the_default_author)
        db.session.add(the_default_user)
        db.session.commit()
        # theadmin = Blog_User.query.all()

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
            theme=themes.themes_data[0]["theme"], picture=pic_src_theme(themes.themes_data[0]["picture"]), picture_source=themes.themes_data[0]["picture_source"])
        theme2 = Blog_Theme(
            theme=themes.themes_data[1]["theme"], picture=pic_src_theme(themes.themes_data[1]["picture"]), picture_source=themes.themes_data[1]["picture_source"])
        theme3 = Blog_Theme(
            theme=themes.themes_data[2]["theme"], picture=pic_src_theme(themes.themes_data[2]["picture"]), picture_source=themes.themes_data[2]["picture_source"])
        theme4 = Blog_Theme(
            theme=themes.themes_data[3]["theme"], picture=pic_src_theme(themes.themes_data[3]["picture"]), picture_source=themes.themes_data[3]["picture_source"])

        db.session.add(theme1)
        db.session.add(theme2)
        db.session.add(theme3)
        db.session.add(theme4)
        db.session.commit()


# Creating dummie accounts: to test and use the app as example
USER_PW = "user123"
USER_ABOUT = authors.authors_about


def create_dummie_accts():
    # Check if dummies exists in the database, if not, add dummie accounts:
    dummies_exists = Blog_User.query.get(4)
    if not dummies_exists:
        random1 = Blog_User(name="Roberta Sanstoms",
                            email="r@r", password=hash_pw(USER_PW), type="admin")
        random2 = Blog_User(name=authors.authors_data[0]["name"], email="e@e", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture=pic_src_user(authors.authors_data[0]["picture"]))
        random3 = Blog_User(name=authors.authors_data[1]["name"], email="j@j", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture=pic_src_user(authors.authors_data[1]["picture"]))
        random4 = Blog_User(name=authors.authors_data[2]["name"], email="m@m", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture=pic_src_user(authors.authors_data[2]["picture"]))
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


# Creating dummie posts: to test and use the app as example
POST_INTRO = posts.post_intro
POST_BODY = posts.post_body
def create_posts():
    # # with current_app.app_context():
    # Check if dummie posts exists in the database, if not, create the posts:
    posts_exist = Blog_Posts.query.get(1)
    if not posts_exist:
        post1 = Blog_Posts(theme_id = posts.post_data[0]["theme"], title = posts.post_data[0]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[0]["author_id"], picture_v=pic_src_post(posts.post_data[0]["picture_v"]), 
                            picture_v_source=posts.post_data[0]["picture_v_source"], picture_h=pic_src_post(posts.post_data[0]["picture_b"]),
                            picture_h_source=posts.post_data[0]["picture_b_source"], picture_s=pic_src_post(posts.post_data[0]["picture_s"]),
                            picture_s_source=posts.post_data[0]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[0]["picture_alt"]),
                            admin_approved= "TRUE")
        post2 = Blog_Posts(theme_id = posts.post_data[1]["theme"], title = posts.post_data[1]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[1]["author_id"], picture_v=pic_src_post(posts.post_data[1]["picture_v"]), 
                            picture_v_source=posts.post_data[1]["picture_v_source"], picture_h=pic_src_post(posts.post_data[1]["picture_b"]),
                            picture_h_source=posts.post_data[1]["picture_b_source"], picture_s=pic_src_post(posts.post_data[1]["picture_s"]),
                            picture_s_source=posts.post_data[1]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[1]["picture_alt"]),
                            admin_approved= "TRUE")
        post3 = Blog_Posts(theme_id = posts.post_data[2]["theme"], title = posts.post_data[2]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[2]["author_id"], picture_v=pic_src_post(posts.post_data[2]["picture_v"]), 
                            picture_v_source=posts.post_data[2]["picture_v_source"], picture_h=pic_src_post(posts.post_data[2]["picture_b"]),
                            picture_h_source=posts.post_data[2]["picture_b_source"], picture_s=pic_src_post(posts.post_data[2]["picture_s"]),
                            picture_s_source=posts.post_data[2]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[2]["picture_alt"]),
                            admin_approved= "TRUE")
        post4 = Blog_Posts(theme_id = posts.post_data[3]["theme"], title = posts.post_data[3]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[3]["author_id"], picture_v=pic_src_post(posts.post_data[3]["picture_v"]), 
                            picture_v_source=posts.post_data[3]["picture_v_source"], picture_h=pic_src_post(posts.post_data[3]["picture_b"]),
                            picture_h_source=posts.post_data[3]["picture_b_source"], picture_s=pic_src_post(posts.post_data[3]["picture_s"]),
                            picture_s_source=posts.post_data[3]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[3]["picture_alt"]),
                            admin_approved= "TRUE")
        post5 = Blog_Posts(theme_id = posts.post_data[4]["theme"], title = posts.post_data[4]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[4]["author_id"], picture_v=pic_src_post(posts.post_data[4]["picture_v"]), 
                            picture_v_source=posts.post_data[4]["picture_v_source"], picture_h=pic_src_post(posts.post_data[4]["picture_b"]),
                            picture_h_source=posts.post_data[4]["picture_b_source"], picture_s=pic_src_post(posts.post_data[4]["picture_s"]),
                            picture_s_source=posts.post_data[4]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[4]["picture_alt"]),
                            admin_approved= "TRUE")
        post6 = Blog_Posts(theme_id = posts.post_data[5]["theme"], title = posts.post_data[5]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[5]["author_id"], picture_v=pic_src_post(posts.post_data[5]["picture_v"]), 
                            picture_v_source=posts.post_data[5]["picture_v_source"], picture_h=pic_src_post(posts.post_data[5]["picture_b"]),
                            picture_h_source=posts.post_data[5]["picture_b_source"], picture_s=pic_src_post(posts.post_data[5]["picture_s"]),
                            picture_s_source=posts.post_data[5]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[5]["picture_alt"]),
                            admin_approved= "TRUE")
        post7 = Blog_Posts(theme_id = posts.post_data[6]["theme"], title = posts.post_data[6]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[6]["author_id"], picture_v=pic_src_post(posts.post_data[6]["picture_v"]), 
                            picture_v_source=posts.post_data[6]["picture_v_source"], picture_h=pic_src_post(posts.post_data[6]["picture_b"]),
                            picture_h_source=posts.post_data[6]["picture_b_source"], picture_s=pic_src_post(posts.post_data[6]["picture_s"]),
                            picture_s_source=posts.post_data[6]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[6]["picture_alt"]),
                            admin_approved= "TRUE")
        post8 = Blog_Posts(theme_id = posts.post_data[7]["theme"], title = posts.post_data[7]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[7]["author_id"], picture_v=pic_src_post(posts.post_data[7]["picture_v"]), 
                            picture_v_source=posts.post_data[7]["picture_v_source"], picture_h=pic_src_post(posts.post_data[7]["picture_b"]),
                            picture_h_source=posts.post_data[7]["picture_b_source"], picture_s=pic_src_post(posts.post_data[7]["picture_s"]),
                            picture_s_source=posts.post_data[7]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[7]["picture_alt"]),
                            admin_approved= "TRUE")
        post9 = Blog_Posts(theme_id = posts.post_data[8]["theme"], title = posts.post_data[8]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[8]["author_id"], picture_v=pic_src_post(posts.post_data[8]["picture_v"]), 
                            picture_v_source=posts.post_data[8]["picture_v_source"], picture_h=pic_src_post(posts.post_data[8]["picture_b"]),
                            picture_h_source=posts.post_data[8]["picture_b_source"], picture_s=pic_src_post(posts.post_data[8]["picture_s"]),
                            picture_s_source=posts.post_data[8]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[8]["picture_alt"]),
                            admin_approved= "TRUE")
        post10 = Blog_Posts(theme_id = posts.post_data[9]["theme"], title = posts.post_data[9]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[9]["author_id"], picture_v=pic_src_post(posts.post_data[9]["picture_v"]), 
                            picture_v_source=posts.post_data[9]["picture_v_source"], picture_h=pic_src_post(posts.post_data[9]["picture_b"]),
                            picture_h_source=posts.post_data[9]["picture_b_source"], picture_s=pic_src_post(posts.post_data[9]["picture_s"]),
                            picture_s_source=posts.post_data[9]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[9]["picture_alt"]),
                            admin_approved= "TRUE")
        post11 = Blog_Posts(theme_id=posts.post_data[10]["theme"], title=posts.post_data[10]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[10]["author_id"], picture_v=pic_src_post(posts.post_data[10]["picture_v"]),
                            picture_v_source=posts.post_data[10]["picture_v_source"], picture_h=pic_src_post(posts.post_data[10]["picture_b"]),
                            picture_h_source=posts.post_data[10]["picture_b_source"], picture_s=pic_src_post(posts.post_data[10]["picture_s"]),
                            picture_s_source=posts.post_data[10]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[10]["picture_alt"]),
                            admin_approved= "TRUE")
        post12 = Blog_Posts(theme_id=posts.post_data[11]["theme"], title=posts.post_data[11]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[11]["author_id"], picture_v=pic_src_post(posts.post_data[11]["picture_v"]),
                            picture_v_source=posts.post_data[11]["picture_v_source"], picture_h=pic_src_post(posts.post_data[11]["picture_b"]),
                            picture_h_source=posts.post_data[11]["picture_b_source"], picture_s=pic_src_post(posts.post_data[11]["picture_s"]),
                            picture_s_source=posts.post_data[11]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[11]["picture_alt"]),
                            admin_approved= "TRUE")
        post13 = Blog_Posts(theme_id=posts.post_data[12]["theme"], title=posts.post_data[12]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[12]["author_id"], picture_v=pic_src_post(posts.post_data[12]["picture_v"]),
                            picture_v_source=posts.post_data[12]["picture_v_source"], picture_h=pic_src_post(posts.post_data[12]["picture_b"]),
                            picture_h_source=posts.post_data[12]["picture_b_source"], picture_s=pic_src_post(posts.post_data[12]["picture_s"]),
                            picture_s_source=posts.post_data[12]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[12]["picture_alt"]))
        post14 = Blog_Posts(theme_id=posts.post_data[13]["theme"], title=posts.post_data[13]["title"], intro=POST_INTRO,
                            body=POST_BODY, author_id=posts.post_data[13]["author_id"], picture_v=pic_src_post(posts.post_data[13]["picture_v"]),
                            picture_v_source=posts.post_data[13]["picture_v_source"], picture_h=pic_src_post(posts.post_data[13]["picture_b"]),
                            picture_h_source=posts.post_data[13]["picture_b_source"], picture_s=pic_src_post(posts.post_data[13]["picture_s"]),
                            picture_s_source=posts.post_data[13]["picture_s_source"], picture_alt=pic_src_post(posts.post_data[13]["picture_alt"]))
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

def create_comments():
    comments_exist = Blog_Comments.query.get(1)
    if not comments_exist:
        comment1 = Blog_Comments(text="I am a test comment", post_id=1, user_id=1)
        comment2 = Blog_Comments(text="I am a test comment", post_id=2, user_id=2)
        comment3 = Blog_Comments(text="I am another test comment", post_id=2, user_id=4, date_submitted=datetime.strptime("2023-02-01 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment4 = Blog_Comments(text="I am a blocked comment", post_id=2, user_id=4, blocked="TRUE")
        comment5 = Blog_Replies(text="I am a reply comment", post_id=2, user_id=5, comment_id=3, date_submitted=datetime.strptime("2023-02-02 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment6 = Blog_Replies(text="Replying again", post_id=2, user_id=4, comment_id=3, date_submitted=datetime.strptime("2023-02-03 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment7 = Blog_Replies(text="Replying", post_id=2, user_id=5, comment_id=3, date_submitted=datetime.strptime("2023-02-04 00:10:00", '%Y-%m-%d %H:%M:%S'))
        comment8 = Blog_Replies(text="Replying back", post_id=2, user_id=5, comment_id=3, blocked="TRUE", date_submitted=datetime.strptime("2023-02-05 00:10:00", '%Y-%m-%d %H:%M:%S'))
        db.session.add(comment1)
        db.session.add(comment2)
        db.session.add(comment3)
        db.session.add(comment4)
        db.session.add(comment5)
        db.session.add(comment6)
        db.session.add(comment7)
        db.session.add(comment8)
        db.session.commit()
        for i in range(8):
            update_stats_comments_total()
    
def create_likes_and_bookmarks():
    likes_exist = Blog_Likes.query.get(1)
    if not likes_exist:
        like1 = Blog_Likes(post_id=2, user_id=4)
        like2 = Blog_Likes(post_id=2, user_id=5)
        bookmark1 = Blog_Bookmarks(post_id=2, user_id=1)
        db.session.add(like1)
        db.session.add(like2)
        db.session.add(bookmark1)
        db.session.commit()
