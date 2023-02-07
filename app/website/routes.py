from flask import Blueprint, render_template, request, current_app
from app.extensions import db
from app.website.posts import the_posts
from app.website.themes import the_themes
from app.website.authors import the_authors
from app.website.contact import send_email
from app.models.contact import Blog_Contact
import copy
from flask_login import current_user


website = Blueprint('website', __name__)

# Blog website pages: Home Page, All posts, About, Contact page
# Routes available for registered and non-registered users alike

@website.route("/")
def home():
    posts_all = copy.deepcopy(the_posts)
    for post in posts_all:
        post.update(
            {"picture_big": f"../static/Pictures_Posts/{post['picture_big']}",
             "picture_small": f"../static/Pictures_Posts/{post['picture_small']}"}
        )
    posts_themes = [
        [post["theme"], f"../static/Pictures_Themes/{post['picture']}", post["id"]] for post in the_themes]
    return render_template('index.html', posts_all=posts_all, posts_themes=posts_themes, logged_in=current_user.is_authenticated)


@website.route("/all/<int:index>")
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

    return render_template('all_posts.html', all_blog_posts=all_blog_posts, chosen_theme=chosen_theme, logged_in=current_user.is_authenticated)


@website.route("/about/")
def about():
    authors_all = copy.deepcopy(the_authors)
    for author in authors_all:
        author.update(
            {"picture": f"../static/Pictures_Users/{author['picture']}",
             })
    return render_template('about.html', authors_all=authors_all, logged_in=current_user.is_authenticated)


@website.route("/contact/", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
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

    return render_template('contact.html', msg_sent=False, logged_in=current_user.is_authenticated)


@website.route("/post/<int:index>")
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

    return render_template('post.html', blog_posts=blog_posts, post_author=post_author, logged_in=current_user.is_authenticated)



