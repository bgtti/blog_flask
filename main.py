from flask import Flask, render_template, request, redirect, flash, url_for
from posts import the_posts
from themes import the_themes
from authors import the_authors
import copy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask_wtf import FlaskForm # login form
from wtforms import StringField, PasswordField, SubmitField  # login form
from wtforms.validators import DataRequired  # login form
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from contact import send_email
from helpers import hash_pw
from werkzeug.security import generate_password_hash, check_password_hash  # used in login


app = Flask(__name__)
app.config['SECRET_KEY'] = "myFlaskApp4Fun"  # needed for login with wtforms

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///admin.db'
app.config['SQLALCHEMY_BINDS'] = {
    'author': 'sqlite:///author.db', 'user': 'sqlite:///user.db', 'theme': 'sqlite:///theme.db', 'posts': 'sqlite:///posts.db', 'contact': 'sqlite:///contact.db'}
db = SQLAlchemy(app) #initializes database

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Blog_User.query.get(int(user_id))

class Blog_User(UserMixin, db.Model):
    __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
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

    def __repr__(self):
        return f"<User: {self.id} {self.name} {self.email}>"

# Create DB module for contact (stores messages sent via contact form)
class Blog_Contact(db.Model):
    __bind_key__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(700))

#     # Create function to create a string
#     def __repr__(self):
#         return '<Name_Message %r>' % self.id



# example to include foreign key:
# employees = Table(
#     "employees",
#     metadata_obj,
#     Column("employee_id", Integer, primary_key=True),
#     Column("employee_name", String(60), nullable=False),
#     Column("employee_dept", Integer, ForeignKey("departments.department_id")),
# )

with app.app_context():
    db.create_all()
    # Check if a super_admin exists in the database, if not, add it:
    super_admin_exists = Blog_User.query.get(1)
    if not super_admin_exists:
        ADMIN_PW = hash_pw("admin123")
        the_super_admin = Blog_User(
            name="Super Admin", email="super@admin", password=ADMIN_PW, type="super_admin")
        db.session.add(the_super_admin)
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
    # my_contacts = db.session.query(Blog_Contact).all()
    # print(my_contacts)
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

        theuser = Blog_User.query.all()
        print(theuser)

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


if __name__ == "__main__":
    app.run(debug=True)

# Dont forget to add possibility of password recovery