from flask import current_app
from app.extensions import db
from app.models.user import Blog_User
from app.models.posts import Blog_Posts
from app.models.text import about_text_author, about_text_user  # dummie strings
from app.account.helpers import hash_pw


# Creating a super_admin and a default author account
# The super_admin is important as this will enable the management of all other users.
# The default author is created for the case of an author having his/her account deleted: the posts
# created by this user will be passed onto the default author's account, to avoid loss of online content.
# you can re-define the log-in credentials for these users by changing the variables bellow.
ADMIN_PW = "admin123"
ADMIN_EMAIL = "super@admin"
ADMIN_NAME = "Super Admin"
DEFAULT_AUTHOR_PW = "author123"
DEFAULT_AUTHOR_EMAIL = "t@t"
DEFAULT_AUTHOR_NAME = "The Travel Blog Team"
DEFAULT_AUTHOR_ABOUT = about_text_author
DEFAULT_AUTHOR_PICTURE = "Picture_default.jpg"

def create_admin_acct():
    # Check if a super_admin exists in the database, if not, add it:
    super_admin_exists = Blog_User.query.get(1)
    if not super_admin_exists:
        the_super_admin = Blog_User(
            name=ADMIN_NAME, email=ADMIN_EMAIL, password=hash_pw(ADMIN_PW), type="super_admin")
        the_default_author = Blog_User(name=DEFAULT_AUTHOR_NAME, email=DEFAULT_AUTHOR_EMAIL, password=hash_pw(DEFAULT_AUTHOR_PW),
                                    type="author", about=DEFAULT_AUTHOR_ABOUT, picture=DEFAULT_AUTHOR_PICTURE)
        db.session.add(the_super_admin)
        db.session.add(the_default_author)
        db.session.commit()
        # theadmin = Blog_User.query.all()


# Creating dummie accounts: to test and use the app as example
USER_PW = "user123"
USER_ABOUT = about_text_user


def create_dummie_accts():
    # Check if dummies exists in the database, if not, add dummie accounts:
    dummies_exists = Blog_User.query.get(3)
    if not dummies_exists:
        random1 = Blog_User(name="Roberta Sanstoms",
                            email="r@r", password=hash_pw(USER_PW), type="admin")
        random2 = Blog_User(name="Elisa S.", email="e@e", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture="Picture_author_1.jpg")
        random3 = Blog_User(name="Ricardo J. F.", email="j@j", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture="Picture_author_2.jpg")
        random4 = Blog_User(name="Martha P.", email="m@m", password=hash_pw(USER_PW),
                            type="author", about=USER_ABOUT, picture="Picture_author_3.jpg")
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

# Creating dummie posts: to test and use the app as example

def create_posts():
    # # with current_app.app_context():
    # Check if dummie posts exists in the database, if not, create the posts:
    posts_exist = Blog_Posts.query.get(1)
    if not posts_exist:
        post1 = Blog_Posts(theme="Beach", title="Cool post", intro="About this",
                        body="This is the body of the post.", author_id=6)
        post2 = Blog_Posts(theme="City", title="Cool post 2", intro="About this again",
                        body="This is the body of the 2nd post.", author_id=4)
        post3 = Blog_Posts(theme="Beach", title="Kinda cool post", intro="About that",
                        body="This is the body of another post.", author_id=4)
        post4 = Blog_Posts(theme="City", title="Kinda cool post", intro="About that",
                        body="This is the body of another post.", author_id=2)
        post5 = Blog_Posts(theme="Beach", title="Kinda cool post", intro="About that",
                        body="This is the body of another post.", author_id=5)
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.add(post4)
        db.session.add(post5)
        db.session.commit()
