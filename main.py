from flask import Flask, render_template, request, redirect, flash, url_for
from posts import the_posts
from themes import the_themes
from authors import the_authors
import copy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask_wtf import FlaskForm # login form
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, SelectField  # login form
from wtforms.validators import DataRequired  # login form
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from contact import send_email
from helpers import hash_pw
from werkzeug.security import generate_password_hash, check_password_hash  # used in login
from flask_ckeditor import CKEditor, CKEditorField #add new blog posts


app = Flask(__name__)
ckeditor = CKEditor(app) #adding ck editor
app.config['SECRET_KEY'] = "myFlaskApp4Fun"  # needed for login with wtforms

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_BINDS'] = {
#     'blog_author': 'sqlite:///blog_author.db', 'blog_user': 'sqlite:///blog_user.db', 'blog_theme': 'sqlite:///blog_theme.db', 'blog_posts': 'sqlite:///blog_posts.db', 'blog_contact': 'sqlite:///blog_contact.db'}
db = SQLAlchemy(app) #initializes database

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Blog_User.query.get(int(user_id))

class Blog_User(UserMixin, db.Model):
    __tablename__ = "blog_user"
    # __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    about = db.Column(db.String(700), default="")
    # in future, change picture to BLOB
    picture = db.Column(db.String(200), default="Picture_default.jpg")
    # type can be: admin, super_admin, author, or user
    type = db.Column(db.String(100), nullable=False, default="user")
    comment = db.Column(db.String(700), default="")
    # whether user has been blocked (future implementation)
    blocked = db.Column(db.String(5), default="FALSE")
    likes = db.Column(db.Integer, default=0)
    # posts = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    posts = db.relationship('Blog_Posts', backref='author')

    def __repr__(self):
        return f"<User: {self.id} {self.name} {self.email}>"

# Blog Posts
class Blog_Posts(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(200), nullable=False)
    # author = db.Column(db.String(200), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    date_to_post = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    picture_v = db.Column(db.String(200))
    picture_v_source = db.Column(db.String(500))
    picture_h = db.Column(db.String(200))
    picture_h_source = db.Column(db.String(500))
    picture_s = db.Column(db.String(200))
    picture_s_source = db.Column(db.String(500))
    picture_alt = db.Column(db.String(200))
    meta_tag = db.Column(db.String(200))
    title_tag = db.Column(db.String(200))
    admin_approved = db.Column(db.String(5), default="FALSE")
    featured = db.Column(db.String(5), default="FALSE")
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    # blog_user = db.relationship('Blog_User', backref='the_author')
    author_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))

    def __repr__(self):
        return f"<Post: {self.id} {self.theme} {self.title}>"

# Create DB module for contact (stores messages sent via contact form)
class Blog_Contact(db.Model):
    __tablename__ = "blog_contact"
    # __bind_key__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(700))

#     # Create function to create a string
#     def __repr__(self):
#         return '<Name_Message %r>' % self.id


with app.app_context():
    db.create_all()
    # Check if a super_admin exists in the database, if not, add it:
    super_admin_exists = Blog_User.query.get(1)
    if not super_admin_exists:
        ADMIN_PW = hash_pw("admin123")
        the_super_admin = Blog_User(
            name="Super Admin", email="super@admin", password=ADMIN_PW, type="super_admin")
        db.session.add(the_super_admin)
        # db.session.commit()
        # creating some dummie accounts (for testing, delete the bellow later):
        RANDOM_PW = hash_pw("user123")
        random1 = Blog_User(name="Maria", email="m@m", password=RANDOM_PW, type="author")
        random2 = Blog_User(name="John Meyers", email="j@m", password=RANDOM_PW, type="author")
        random3 = Blog_User(name="Fabienne123", email="f@f", password=RANDOM_PW, type="user")
        random4 = Blog_User(name="Kokaloka", email="k@k", password=RANDOM_PW, type="user")
        random5 = Blog_User(name="SublimePoster", email="s@p", password=RANDOM_PW, type="user")
        # creating dummie posts (for testing, delete the bellow later):
        post1 = Blog_Posts(theme="Beach", title="Cool post", intro="About this", body="This is the body of the post.", author_id=2)
        post2 = Blog_Posts(theme="City", title="Cool post 2", intro="About this again", body="This is the body of the 2nd post.", author_id=3)
        post3 = Blog_Posts(theme="City", title="Kinda cool post", intro="About that", body="This is the body of another post.", author_id=2)
        db.session.add(random1)
        db.session.add(random2)
        db.session.add(random3)
        db.session.add(random4)
        db.session.add(random5)
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.commit()
    theadmin = Blog_User.query.all()


# ***********************************************************************************************
# BLOG PAGES
@app.route("/")
def home():
    posts_all = copy.deepcopy(the_posts)
    for post in posts_all:
        post.update(
            {"picture_big": f"../static/Pictures_Posts/{post['picture_big']}",
             "picture_small": f"../static/Pictures_Posts/{post['picture_small']}"}
        )
    posts_themes = [
        [post["theme"], f"../static/Pictures_Themes/{post['picture']}", post["id"]] for post in the_themes]
    return render_template('index.html', posts_all=posts_all, posts_themes=posts_themes)
    # return render_template('index.html', posts_all=posts_all, posts_themes=posts_themes, logged_in=current_user.is_authenticated)

@app.route("/all/<int:index>")
def all(index):
    all_blog_posts = []
    chosen_theme = ""
    if index != 0:
        for theme in the_themes:
            if theme["id"] == index:
                chosen_theme = theme["theme"]

    for post in the_posts:

        if index != 0 and post["theme"] != chosen_theme:
            continue
        else:
            post_at_hand = dict(post)
            intro = f"{post_at_hand['intro'][:300]}..."
            post_at_hand.update(
                {"picture_big": f"../static/Pictures_Posts/{post_at_hand['picture_big']}",
                 "picture_small": f"../static/Pictures_Posts/{post_at_hand['picture_small']}",
                "intro": intro}
            )
            all_blog_posts.append(post_at_hand)
    
    return render_template('all_posts.html', all_blog_posts=all_blog_posts, chosen_theme=chosen_theme)

@app.route("/about/")
def about():
    authors_all = copy.deepcopy(the_authors)
    for author in authors_all:
        author.update(
            {"picture": f"../static/Pictures_Users/{author['picture']}",
        })
    return render_template('about.html', authors_all=authors_all)


@app.route("/contact/", methods=['POST', 'GET'])
def contact():
    if request.method=="POST":
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        contact_message = request.form['contact_message']
        new_contact = Blog_Contact(
            name=contact_name, email=contact_email, message=contact_message)
        try:
            # push to database:
            db.session.add(new_contact)
            db.session.commit()
            # send email:
            send_email(contact_name, contact_email, contact_message)
            return render_template('contact.html', msg_sent=True)
        except:
            return "There was an error adding message to the database."
    
    return render_template('contact.html', msg_sent=False)

@app.route("/post/<int:index>")
def blog_post(index):
    blog_posts = copy.deepcopy(the_posts)
    post_author = None
    for post in blog_posts:
        if post["id"] == index:
            blog_posts = post
            blog_posts.update(
                {"picture_big": f"../static/Pictures_Posts/{post['picture_big']}",
                 "picture_small": f"../static/Pictures_Posts/{post['picture_small']}"})
            for author in the_authors:
                if author["name"] == post["author"]:
                    post_author = dict(author)
                    post_author.update({
                        "picture": f"../static/Pictures_Author/{author['picture']}"
                    })

    return render_template('post.html', blog_posts=blog_posts, post_author=post_author)

# ***********************************************************************************************
# Admin Area (might be deleted)
class AdminSignInForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')

@app.route("/adminlogin", methods=['GET', 'POST'])
def admin_login():
    form = AdminSignInForm()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.password.data == "12345678":
            return render_template("admindashboard.html")
        else:
            return render_template('adminlogin.html', form=form, login_failure=True)
    return render_template('adminlogin.html', form=form, login_failure=False)

@app.route("/admindashboard")
def admin_dashboard():
    return render_template('admindashboard.html')

# ***********************************************************************************************
# User log in area

@app.route("/dashboard")
@login_required
def user_dashboard():
    print(current_user.name)
    return render_template('user_dashboard.html', name=current_user.name, logged_in=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#SIGN UP and LOG IN
@app.route("/signup", methods=["GET", "POST"])
def user_signup():
    # in the future, check if username is unique
    if request.method == "POST":
        if Blog_User.query.filter_by(email=request.form.get("email")).first():
            #if user already exists:
            flash("This email is already registered with us. Log-in instead!")
            return redirect(url_for("user_login"))

        new_user = Blog_User(
            name=request.form.get("username"),
            email=request.form.get("email"),
            password=hash_pw(request.form.get("password")),
            type="user"
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('user_dashboard'))

    return render_template('signup.html', logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        the_user = Blog_User.query.filter_by(email=email).first()
        # wrong email:
        if not the_user:
            flash("This email does not exist in our database.")
            return redirect(url_for("user_login"))
        # wrong password:
        elif not check_password_hash(the_user.password, password):
            flash("Incorrect password, please try again.")
            return redirect(url_for("user_login"))
        # email exists and password is correct
        else: 
            login_user(the_user)
            return redirect(url_for('user_dashboard'))
    return render_template("login.html", logged_in=current_user.is_authenticated)

# ***********************************************************************************************
# Super admin: ability to manage users

@app.route("/user_dashboard/manage_users", methods=["GET", "POST"])
@login_required
def manage_users():
    all_blog_users = Blog_User.query.order_by(Blog_User.id)
    return render_template("manage_users.html", logged_in=current_user.is_authenticated, all_blog_users=all_blog_users)

@app.route("/user_dashboard/manage_users/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_users(id):
    acct_types = ["admin", "author", "user"]
    acct_blocked = ["FALSE", "TRUE"]
    user_to_update = Blog_User.query.get_or_404(id)

    if request.method == "POST":
        if Blog_User.query.filter(Blog_User.id != id, Blog_User.email == request.form.get("email_update")).first():
            flash("This email is already registered with us.")
            return render_template("manage_users_update.html", id=user_to_update.id, logged_in=current_user.is_authenticated, user_to_update=user_to_update, acct_types=acct_types, acct_blocked=acct_blocked)
        elif Blog_User.query.filter(Blog_User.id != id, Blog_User.name == request.form.get("username_update")).first():
            flash("This username is already registered with us.")
            return render_template("manage_users_update.html", id=user_to_update.id, logged_in=current_user.is_authenticated, user_to_update=user_to_update, acct_types=acct_types, acct_blocked=acct_blocked)
        else:
            user_to_update.name = request.form.get("username_update")
            user_to_update.email = request.form.get("email_update")
            user_to_update.type = request.form.get("accttype_update")
            user_to_update.blocked = request.form.get("acctblocked_update")
            try:
                db.session.commit()
                flash("User updated successfully!")
                # no time for flash, change way of displaying success
                return redirect(url_for('manage_users'))
            except:
                flash("Error, try again.")
                return render_template("manage_users_update.html", id=user_to_update.id, logged_in=current_user.is_authenticated, user_to_update=user_to_update, acct_types=acct_types, acct_blocked=acct_blocked)
    else:
        return render_template("manage_users_update.html", logged_in=current_user.is_authenticated, user_to_update=user_to_update, acct_types=acct_types, acct_blocked=acct_blocked)


@app.route("/user_dashboard/manage_users/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_users(id):
    user_to_delete = Blog_User.query.get_or_404(id)
    if request.method == "POST":
        if id == 1:
            flash("Authorization error: this user cannot be deleted")
        else:
            try:
                db.session.delete(user_to_delete)
                db.session.commit()
                flash("User deleted successfully.")
                return redirect(url_for('manage_users'))
            except:
                flash("There was a problem deleting this user.")
                return render_template("manage_users_delete.html", logged_in=current_user.is_authenticated, user_to_delete=user_to_delete)
    else:
        return render_template("manage_users_delete.html", logged_in=current_user.is_authenticated, user_to_delete=user_to_delete)

# ***********************************************************************************************
# Blog posts form
class The_Posts(FlaskForm):
    theme = SelectField(u'Theme', choices=['Beach', 'City', 'Nature', 'Culture'])
    author = StringField("Author")
    date = DateTimeField('Date', default=datetime.now, format='%Y-%m-%d')
    title = StringField("Title", validators=[DataRequired()])
    intro = StringField("Intro", validators=[DataRequired()])
    # body = StringField("Body", validators=[DataRequired()], widget=TextArea())
    body = CKEditorField("Body", validators=[DataRequired()])
    picture_v = StringField("Picture Vertical", default="Picture_v_XX.jpg", validators=[DataRequired()])
    picture_v_source = StringField("Picture Vertical", default="http://")
    picture_h = StringField("Picture Horizontal", default="Picture_h_XX.jpg", validators=[DataRequired()])
    picture_h_source = StringField("Picture Vertical", default="http://")
    picture_s = StringField("Picture Squared", default="Picture_s_XX.jpg", validators=[DataRequired()])
    picture_s_source = StringField("Picture Vertical", default="http://")
    picture_alt = StringField("Picture Alt Text", validators=[DataRequired()])
    meta_tag = StringField("Meta Tag", validators=[DataRequired()])
    title_tag = StringField("Title Tag", validators=[DataRequired()])
    submit =  SubmitField()

# Adding a new blog post
@app.route("/user_dashboard/submit_posts", methods=["GET", "POST"])
@login_required
def submit_post():
    form = The_Posts()
    # POST NOT BEING SUBMITTED ON 'SUBMIT'
    if form.validate_on_submit():
        print("now here")
        author = current_user.id
        post = Blog_Posts(theme=form.theme.data,
                            date_to_post=form.date.data, title=form.title.data, intro=form.intro.data,
                            body=form.body.data, picture_v=form.picture_v.data, picture_v_source=form.picture_v_source.data,
                            picture_h=form.picture_h.data, picture_h_source=form.picture_h_source.data,
                            picture_s=form.picture_s.data, picture_s_source=form.picture_s_source.data, 
                            picture_alt=form.picture_alt.data, meta_tag=form.meta_tag.data, title_tag=form.title_tag.data, 
                            author_id=author)
        # clear form:
        form.theme.data = ""
        # form.author.data = ""
        form.date.data = datetime.now
        form.title.data = ""
        form.intro.data = ""
        form.body.data = ""
        form.picture_v.data = ""
        form.picture_v_source.data= ""
        form.picture_h.data = ""
        form.picture_h_source.data = ""
        form.picture_s.data = ""
        form.picture_s_source.data = ""
        form.picture_alt.data = ""
        form.meta_tag.data = ""
        form.title_tag.data = ""
        #add to database:
        db.session.add(post)
        db.session.commit()

        flash("Blog post submitted sucessfully!")

    return render_template("submit_post.html", logged_in=current_user.is_authenticated, form=form)


# Seeing all submitted posts
@app.route("/user_dashboard/submitted_posts")
@login_required
def submitted_posts():
    all_blog_posts_submitted = Blog_Posts.query.order_by(Blog_Posts.id)
    return render_template("submitted_blog_posts.html", logged_in=current_user.is_authenticated, all_blog_posts_submitted=all_blog_posts_submitted)

# Previewing a post
@app.route("/user_dashboard/preview_post/<int:id>")
@login_required
def preview_post(id):
    post_to_preview = Blog_Posts.query.get_or_404(id)
    return render_template("preview_post.html", logged_in=current_user.is_authenticated, post_to_preview=post_to_preview)

# Editing a post
@app.route("/user_dashboard/editting_post/<int:id>", methods=["GET", "POST"])
@login_required
def editing_posts(id):
    post_to_edit = Blog_Posts.query.get_or_404(id)
    form = The_Posts()
    # changing the post
    if form.validate_on_submit():
        post_to_edit.theme = form.theme.data
        # post_to_edit.author = form.author.data #author not available anymore, use author_id
        post_to_edit.date_to_post = form.date.data
        post_to_edit.title = form.title.data
        post_to_edit.intro = form.intro.data
        post_to_edit.body = form.body.data
        post_to_edit.picture_v = form.picture_v.data
        post_to_edit.picture_v_source = form.picture_v_source.data
        post_to_edit.picture_h = form.picture_h.data
        post_to_edit.picture_h_source = form.picture_h_source.data
        post_to_edit.picture_s = form.picture_s.data
        post_to_edit.picture_s_source = form.picture_s_source.data
        post_to_edit.picture_alt = form.picture_alt.data
        post_to_edit.meta_tag = form.meta_tag.data
        post_to_edit.title_tag = form.title_tag.data
        # add to database:
        db.session.add(post_to_edit)
        db.session.commit()
        flash("Post has been updated successfully!")
        return redirect(url_for("submitted_posts", logged_in=current_user.is_authenticated))
    # filling out the form with saved post data
    form.theme.data = post_to_edit.theme
    form.author.data = post_to_edit.author.name
    form.date.data = post_to_edit.date_to_post
    form.title.data = post_to_edit.title
    form.intro.data = post_to_edit.intro
    form.body.data = post_to_edit.body
    form.picture_v.data = post_to_edit.picture_v
    form.picture_v_source.data = post_to_edit.picture_v_source
    form.picture_h.data = post_to_edit.picture_h
    form.picture_h_source.data = post_to_edit.picture_h_source
    form.picture_s.data = post_to_edit.picture_s
    form.picture_s_source.data = post_to_edit.picture_s_source
    form.picture_alt.data = post_to_edit.picture_alt
    form.meta_tag.data = post_to_edit.meta_tag
    form.title_tag.data = post_to_edit.title_tag
    return render_template('editing_post.html', logged_in=current_user.is_authenticated, form=form)

# Deleting a post
@app.route("/user_dashboard/deleting_post/<int:id>", methods=["GET", "POST"])
@login_required
def deleting_posts(id):
    post_to_delete = Blog_Posts.query.get_or_404(id)
    if request.method == "POST":
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post deleted successfully.")
            return redirect(url_for('submitted_posts'))
        except:
            flash("There was a problem deleting this post.")
            return render_template("manage_posts_delete.html", logged_in=current_user.is_authenticated, post_to_delete=post_to_delete)
    else:
        return render_template("manage_posts_delete.html", logged_in=current_user.is_authenticated, post_to_delete=post_to_delete)

# ***********************************************************************************************
# Manage Own Account

@app.route("/user_dashboard/manage_account")
@login_required
def manage_acct():
    return render_template("manage_acct.html", logged_in=current_user.is_authenticated)


@app.route("/user_dashboard/manage_acct/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_own_acct_info(id):
    user_at_hand = Blog_User.query.get_or_404(id)

    if request.method == "POST":
        user_at_hand.name = request.form.get("username_update")
        user_at_hand.email = request.form.get("email_update")
        user_at_hand.about = request.form.get("about_update")
        try:
            db.session.commit()
            flash("Acct info updated successfully!")
            # no time for flash, change way of displaying success
            return redirect(url_for('manage_acct'))
        except:
            flash("Oops, error, try again.")
            return redirect(url_for('manage_acct'))
    else:
        return render_template("manage_acct_update.html", logged_in=current_user.is_authenticated)


@app.route("/user_dashboard/manage_acct/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_own_acct(id):
    user_at_hand = Blog_User.query.get_or_404(id)
    if request.method == "POST":
        if id == 1:
            flash("Authorization error: this user cannot be deleted")
        else:
            try:
                db.session.delete(user_at_hand)
                db.session.commit()
                flash("Your acct was deleted successfully.")
                return redirect(url_for("home"))
            except:
                flash("There was a problem deleting your account.")
                return redirect(url_for('manage_acct'))
    else:
        return render_template("manage_acct_delete.html", logged_in=current_user.is_authenticated)
# ***********************************************************************************************
# 404 and 500 Errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)

# Dont forget to add possibility of password recovery