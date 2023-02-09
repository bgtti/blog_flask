from flask import Blueprint, render_template, request, flash
from app.extensions import db
from app.website.contact import send_email
from app.website.forms import The_Comments
from app.models.contact import Blog_Contact
from app.models.themes import Blog_Theme
from app.models.posts import Blog_Posts
from app.models.user import Blog_User
from app.models.comments import Blog_Comments, Blog_Replies
from flask_login import current_user
from datetime import datetime
from sqlalchemy import desc



website = Blueprint('website', __name__)

# Blog website pages: Home Page, All posts, About, Contact page
# Routes available for registered and non-registered users alike

@website.route("/")
def home():
    # query database for themes while getting picture src
    posts_themes = [(u.theme, u.picture, u.id)
                    for u in db.session.query(Blog_Theme).all()]
    theme_list = [t[2] for t in posts_themes]
    
    # query posts to get the latest 3 posts of each theme. 
    # Important note: the code bellow is not maintainable if we increase the number of themes, but I could not achieve a better result on my own.
    # This should be improved.
    # The code also selects the forth theme's query results' ids to identify these posts, as this is the only group of posts displayed separately in index.html
    posts_all = []
    forth_theme_post_ids = []
    for num_themes in theme_list:
        query = db.session.query(Blog_Posts).filter(
                Blog_Posts.admin_approved == "TRUE", Blog_Posts.date_to_post <= datetime.utcnow(),
            Blog_Posts.theme_id == num_themes).order_by(desc(Blog_Posts.date_to_post)).limit(3)
        posts_all.append(query.all())
        if num_themes == 4:
            for this_query in query:
                forth_theme_post_ids.append(this_query.id)
    posts_all = posts_all[0] + posts_all[1] + posts_all[2] + posts_all[3]

    return render_template('index.html', posts_all=posts_all, posts_themes=posts_themes, logged_in=current_user.is_authenticated, forth_theme_post_ids=forth_theme_post_ids)

# route to 'All Posts' page or page by chosen theme
@website.route("/all/<int:index>")
def all(index):
    index = int(index)
    all_blog_posts = None
    chosen_theme = ""
    intros = []
    if index != 0:
        chosen_theme = db.session.query(
            Blog_Theme).filter(Blog_Theme.id == index).first().theme
        all_blog_posts = db.session.query(Blog_Posts).filter(Blog_Posts.theme_id == index,
            Blog_Posts.admin_approved == "TRUE", Blog_Posts.date_to_post <= datetime.utcnow(),
        ).order_by(desc(Blog_Posts.date_to_post)).limit(25)
    else:
        all_blog_posts = db.session.query(Blog_Posts).filter(
            Blog_Posts.admin_approved == "TRUE", Blog_Posts.date_to_post <= datetime.utcnow(),
            ).order_by(desc(Blog_Posts.date_to_post)).limit(25)
    for post in all_blog_posts:
        if len(post.intro) > 300:
            cut_intro_if_too_long = f"{post.intro[:300]}..."
            intros.append(cut_intro_if_too_long)
        else:
            intros.append(post.intro)

    return render_template('all_posts.html', all_blog_posts=all_blog_posts, chosen_theme=chosen_theme, intros=intros, logged_in=current_user.is_authenticated)


@website.route("/about/")
def about():
    authors_all = db.session.query(Blog_User).filter(
        Blog_User.blocked == "FALSE", Blog_User.type == "author",
        ).order_by(desc(Blog_User.id)).limit(25)

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


@website.route("/post/<int:index>", methods=["GET", "POST"])
def blog_post(index):
    # get the post
    blog_post = db.session.query(Blog_Posts).filter(Blog_Posts.id == index,
        Blog_Posts.admin_approved == "TRUE", Blog_Posts.date_to_post <= datetime.utcnow(),
                                                    ).order_by(Blog_Posts.date_submitted.desc()).first()

    # get the comments
    comments = db.session.query(Blog_Comments).filter(
                Blog_Comments.post_id == index).limit(25)

    # get the replies
    replies = db.session.query(Blog_Replies).filter(Blog_Replies.post_id == index,
                ).order_by(Blog_Replies.date_submitted.asc()).limit(100)
    
    # main comments --- order by date
    form = The_Comments()
    if request.method == "POST":
        if form.validate_on_submit():
            this_comment = Blog_Comments(
                text=form.comment.data, post_id=index, user_id=current_user.id)
            #clear form:
            form.comment.data = ""
            # add to database:
            db.session.add(this_comment)
            db.session.commit()
            flash("Comment submitted sucessfully!")
            return render_template('post.html', blog_posts=blog_post, logged_in=current_user.is_authenticated, form=form, comments=comments, replies=replies)

    return render_template('post.html', blog_posts=blog_post, logged_in=current_user.is_authenticated, form=form, comments=comments, replies=replies)


