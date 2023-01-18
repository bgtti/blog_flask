from flask import Flask, render_template, request, redirect
from posts import the_posts
from themes import the_themes
from authors import the_authors
import copy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import smtplib
import os #getting .env
from dotenv import load_dotenv  # .env

app = Flask(__name__)

# EMAIL
load_dotenv() # used to get .env variables, where username and password for the email account are stored
EMAIL = os.getenv('EMAIL_ADDRESS')  # put your email here, used for the sender and receiver
PASSWORD = os.getenv('EMAIL_PASSWORD')  # put your password here

def send_email(form_user_name, form_user_email, form_user_message):
    SUBJECT = f"Subject: Travel Blog New Message from {form_user_name}"
    MESSAGE = f"""\
Contact name: {form_user_name}
Contact email: {form_user_email}
Message:
{form_user_message}
    """
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
                                msg=f"{SUBJECT}\n\n{MESSAGE}")
    except:
        return "There was an error sending your message."


# DATABASE
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///contact.db'
db = SQLAlchemy(app) #initializes database

# Create DB module for contact
class Blog_Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(700))

    # Create function to create a string
    def __repr__(self):
        return '<Name_Message %r>' % self.id

with app.app_context():
    db.create_all()

# BLOG
@app.route("/")
def home():
    posts_all = copy.deepcopy(the_posts)
    for post in posts_all:
        post.update(
            {"picture_big": f"../static/{post['picture_big']}",
            "picture_small": f"../static/{post['picture_small']}"}
        )
    posts_themes = [
        [post["theme"], f"../static/{post['picture']}", post["id"]] for post in the_themes]
    return render_template('index.html', posts_all=posts_all, posts_themes=posts_themes)

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
                {"picture_big": f"../static/{post_at_hand['picture_big']}",
                "picture_small": f"../static/{post_at_hand['picture_small']}",
                "intro": intro}
            )
            all_blog_posts.append(post_at_hand)
    
    return render_template('all_posts.html', all_blog_posts=all_blog_posts, chosen_theme=chosen_theme)

@app.route("/about/")
def about():
    authors_all = copy.deepcopy(the_authors)
    for author in authors_all:
        author.update(
            {"picture": f"../static/{author['picture']}",
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
        print(contact_name)
        print(contact_email)
        print(contact_message)
        try:
            # push to database:
            db.session.add(new_contact)
            db.session.commit()
            # send email:
            send_email(contact_name, contact_email, contact_message)
            return render_template('contact.html', msg_sent=True)
        except:
            return "There was an error adding message to the database."
    my_contacts = db.session.query(Blog_Contact).all()
    print(my_contacts)
    return render_template('contact.html', msg_sent=True)

@app.route("/post/<int:index>")
def blog_post(index):
    blog_posts = copy.deepcopy(the_posts)
    post_author = None
    for post in blog_posts:
        if post["id"] == index:
            blog_posts = post
            blog_posts.update(
                {"picture_big": f"../static/{post['picture_big']}",
                "picture_small": f"../static/{post['picture_small']}"})
            for author in the_authors:
                if author["name"] == post["author"]:
                    post_author = dict(author)
                    post_author.update({
                        "picture": f"../static/{author['picture']}"
                    })

    return render_template('post.html', blog_posts=blog_posts, post_author=post_author)


if __name__ == "__main__":
    app.run(debug=True)
