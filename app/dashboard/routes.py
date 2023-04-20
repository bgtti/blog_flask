from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from app.extensions import db
from app.models.user import Blog_User
from app.models.posts import Blog_Posts
from app.dashboard.forms import The_Posts
from app.dashboard.helpers import check_blog_picture, delete_blog_img
from app.models.themes import Blog_Theme
from app.models.helpers import update_stats_users_active, update_approved_post_stats, change_authorship_of_all_post
from app.models.likes import Blog_Likes
from app.models.bookmarks import Blog_Bookmarks
from app.models.comments import Blog_Comments, Blog_Replies
from app.models.helpers import update_likes, update_bookmarks, delete_comment, delete_reply
from datetime import datetime
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

dashboard = Blueprint('dashboard', __name__)

# Pages: dashboard, etc
# Routes available for all registered users of types admin and author

# ***********************************************************************************************
# USER MANAGEMENT: admin access only
# Managing users: see all users
@dashboard.route("/dashboard/manage_users", methods=["GET", "POST"])
@login_required
def users_table():
    user_type = current_user.type
    if user_type == "admin" or user_type == "super_admin":
        all_blog_users = Blog_User.query.order_by(Blog_User.id)
        return render_template("dashboard/users_table.html", logged_in=current_user.is_authenticated, all_blog_users=all_blog_users)
    else:
        flash("Access denied: admin access only.")
        return redirect(url_for('website.home'))

# Managing users: update user
@dashboard.route("/dashboard/manage_users/update/<int:id>", methods=["GET", "POST"])
@login_required
def user_update(id):
    acct_types = ["admin", "author", "user"]
    acct_blocked = ["FALSE", "TRUE"]
    user_to_update = Blog_User.query.get_or_404(id)

    if request.method == "POST":
        if Blog_User.query.filter(Blog_User.id != id, Blog_User.email == request.form.get("email_update")).first():
            flash("This email is already registered with us.")
            return render_template("dashboard/users_user_update.html", id=user_to_update.id, logged_in=current_user.is_authenticated, user_to_update=user_to_update, acct_types=acct_types, acct_blocked=acct_blocked)
        elif Blog_User.query.filter(Blog_User.id != id, Blog_User.name == request.form.get("username_update")).first():
            flash("This username is already registered with us.")
            return render_template("dashboard/users_user_update.html", id=user_to_update.id, logged_in=current_user.is_authenticated, user_to_update=user_to_update, acct_types=acct_types, acct_blocked=acct_blocked)
        else:
            # if the user to being updated is of type author, if type is updated, posts have to pass to default author first.
            if user_to_update.type == "author":
                if request.form.get("accttype_update") != "author":
                    change_authorship_of_all_post(user_to_update.id, 2)

            user_to_update.name = request.form.get("username_update")
            user_to_update.email = request.form.get("email_update")
            user_to_update.type = request.form.get("accttype_update")
            user_to_update.blocked = request.form.get("acctblocked_update")
            try:
                if request.form.get("acctblocked_update") == "TRUE":
                    user_comments = Blog_Comments.query.filter(
                        Blog_Comments.user_id == user_to_update.id).all()
                    user_replies = Blog_Replies.query.filter(
                        Blog_Replies.user_id == user_to_update.id).all()
                    if user_comments:
                        for comment in user_comments:
                            comment.blocked = "TRUE"
                    if user_replies:
                        for reply in user_replies:
                            reply.blocked = "TRUE"
                if request.form.get("acctblocked_update") == "FALSE":
                    user_comments = Blog_Comments.query.filter(
                        Blog_Comments.user_id == user_to_update.id).all()
                    user_replies = Blog_Replies.query.filter(
                        Blog_Replies.user_id == user_to_update.id).all()
                    if user_comments:
                        for comment in user_comments:
                            comment.blocked = "FALSE"
                    if user_replies:
                        for reply in user_replies:
                            reply.blocked = "FALSE"
                db.session.commit()
                flash("User updated successfully!")
                # no time for flash, change way of displaying success
                return redirect(url_for('dashboard.users_table'))
            except:
                db.session.rollback()
                flash("Error, try again.")
                return render_template("dashboard/users_user_update.html", id=user_to_update.id, logged_in=current_user.is_authenticated, user_to_update=user_to_update, acct_types=acct_types, acct_blocked=acct_blocked)
    else:
        return render_template("dashboard/users_user_update.html", logged_in=current_user.is_authenticated, user_to_update=user_to_update, acct_types=acct_types, acct_blocked=acct_blocked)


# Deleting user
@dashboard.route("/dashboard/manage_users/delete/<int:id>", methods=["GET", "POST"])
@login_required
def user_delete(id):
    user_to_delete = Blog_User.query.get_or_404(id)
    if request.method == "POST":
        if id == 1:
            flash("Authorization error: this user cannot be deleted")
        else:
            try:
                # if user is author, transfer the authorship of the posts to the default author
                if user_to_delete.type == "author":
                    change_authorship_of_all_post(user_to_delete.id, 2)
                # if user has comments/replies, change ownership (to default user of id 3 and delete or mark as blocked ([deleted]).
                if user_to_delete.comments:
                    comments = Blog_Comments.query.filter_by(
                        user_id=user_to_delete.id).all()
                    for comment in comments:
                        comment.user_id = 3
                        delete_comment(comment.id)
                if user_to_delete.replies:
                    replies = comments = Blog_Replies.query.filter_by(
                        user_id=user_to_delete.id).all()
                    for reply in replies:
                        reply.user_id = 3
                        delete_reply(reply.id)
                # delete bookmarks and likes
                if user_to_delete.likes:
                    likes = Blog_Likes.query.filter_by(
                        user_id=user_to_delete.id).all()
                    for like in likes:
                        db.session.delete(like)
                        update_likes(-1)
                if user_to_delete.bookmarks:
                    bookmarks = Blog_Bookmarks.query.filter_by(
                        user_id=user_to_delete.id).all()
                    for bookmark in bookmarks:
                        db.session.delete(bookmark)
                        update_bookmarks(-1)
                # delete user's picture
                if user_to_delete.picture == "" or user_to_delete.picture == "Picture_default.jpg":
                    profile_picture = None
                else:
                    profile_picture = user_to_delete.picture

                if profile_picture != None and os.path.exists(os.path.join(current_app.config["PROFILE_IMG_FOLDER"], profile_picture)):
                    os.remove(os.path.join(
                        current_app.config["PROFILE_IMG_FOLDER"], profile_picture))

                # delete user
                db.session.delete(user_to_delete)
                db.session.commit()
                flash("User deleted successfully.")
                update_stats_users_active(-1)
                return redirect(url_for('dashboard.users_table'))
            except:
                flash("There was a problem deleting this user.")
                db.session.rollback()
                return render_template("dashboard/users_user_delete.html", logged_in=current_user.is_authenticated, user_to_delete=user_to_delete)
    else:
        return render_template("dashboard/users_user_delete.html", logged_in=current_user.is_authenticated, user_to_delete=user_to_delete)

# Blocking user
# Blocking a user will not influence the stats of total active users.
# Blocked users will not be able to log in
@dashboard.route("/dashboard/manage_users/block/<int:id>", methods=["GET", "POST"])
@login_required
def user_block(id):
    user_to_block = Blog_User.query.get_or_404(id)
    if request.method == "POST":
        if id == 1:
            flash("Authorization error: this user cannot be blocked")
        else:
            user_to_block.blocked = "TRUE"
            # all comments and replies shall be blocked
            user_comments = Blog_Comments.query.filter(
                Blog_Comments.user_id == user_to_block.id).all()
            user_replies = Blog_Replies.query.filter(
                Blog_Replies.user_id == user_to_block.id).all()
            if user_comments:
                for comment in user_comments:
                    comment.blocked = "TRUE"
            if user_replies:
                for reply in user_replies:
                    reply.blocked = "TRUE"
            try:
                db.session.commit()
                flash("User blocked successfully.")
                return redirect(url_for('dashboard.users_table'))
            except:
                db.session.rollback()
                flash("There was a problem blocking this user.")
                return render_template("dashboard/users_user_block.html", logged_in=current_user.is_authenticated, user_to_block=user_to_block)
    else:
        return render_template("dashboard/users_user_block.html", logged_in=current_user.is_authenticated, user_to_block=user_to_block)

# Previewing a user's account information
@dashboard.route("/dashboard/manage_users/preview/<int:id>")
@login_required
def user_preview(id):
    user_to_preview = Blog_User.query.get_or_404(id)
    return render_template("dashboard/users_user_preview.html", logged_in=current_user.is_authenticated, user_to_preview=user_to_preview)

# ***********************************************************************************************
# POST MANGEMENT

# ADDING NEW BLOG POST -  AUTHORS ONLY
# Only users of type authors can add new posts
@dashboard.route("/dashboard/submit_new_post", methods=["GET", "POST"])
@login_required
def submit_post():
    themes_list = [(u.id, u.theme) for u in db.session.query(Blog_Theme).all()]
    form = The_Posts(obj=themes_list)
    form.theme.choices = themes_list

    # if request.method == "POST":
    if form.validate_on_submit():
        author = current_user.id
        
        # get all information from the form with the exeption of the blog post pictures
        # this will enable the saving of the information even if there is an error with the picture upload: 
        post = Blog_Posts(theme_id=form.theme.data,
                            date_to_post=form.date.data, title=form.title.data, intro=form.intro.data,
                            body=form.body.data, picture_v_source=form.picture_v_source.data, picture_h_source=form.picture_h_source.data,
                            picture_s_source=form.picture_s_source.data,
                            picture_alt=form.picture_alt.data, meta_tag=form.meta_tag.data, title_tag=form.title_tag.data,
                            author_id=author)
        
        # add form information to database without the pictures:
        try:
            db.session.add(post)
            db.session.commit()
        except:
            flash("Oops, error saving your blog post, check all fields and try again.")
            db.session.rollback()

        # checking images: one image at a time
        the_post_id = post.id

        submit_post_blog_img_provided = dict(v = False, h = False, s = False)
        submit_post_blog_img_status = dict(v=False, h=False, s=False)

        def submit_post_blog_img_handle (img_filename, img_format):
            accepted_img_format = ["v", "h", "s"]
            if img_format not in accepted_img_format:
                raise NameError(
                    "submit_post_blog_img_handle function was supplied an invalid img_format")
            new_img_name = check_blog_picture(
                the_post_id, img_filename, img_format)
            if new_img_name:
                new_img_format = "picture_" + img_format
                the_img = request.files[new_img_format]
                try:
                    the_img.save(os.path.join(
                        current_app.config["BLOG_IMG_FOLDER"], new_img_name))
                    if img_format == "v":
                        post.picture_v = new_img_name
                    elif img_format == "h":
                        post.picture_h = new_img_name
                    else:
                        post.picture_s = new_img_name
                    db.session.commit()
                    submit_post_blog_img_status[img_format] = True
                except:
                    submit_post_blog_img_status[img_format] = False

        # checking picture vertical:
        if form.picture_v.data and int(form.picture_v_size.data) < 1500000:
            img_v_filename = secure_filename(form.picture_v.data.filename)
            submit_post_blog_img_handle(img_v_filename, "v")
            submit_post_blog_img_provided["v"] = True
        else:
            submit_post_blog_img_provided["v"] = False

        # checking picture horizontal:
        if form.picture_h.data and int(form.picture_h_size.data) < 1500000:
            img_h_filename = secure_filename(form.picture_h.data.filename)
            submit_post_blog_img_handle(img_h_filename, "h")
            submit_post_blog_img_provided["h"] = True
        else:
            submit_post_blog_img_provided["h"] = False

        # checking picture squared:
        if form.picture_s.data and int(form.picture_s_size.data) < 1500000:
            img_s_filename = secure_filename(form.picture_s.data.filename)
            submit_post_blog_img_handle(img_s_filename, "s")
            submit_post_blog_img_provided["s"] = True
        else:
            submit_post_blog_img_provided["s"] = False

        # inform the user of the status of the post
        submit_post_blog_missing_pic = False
        submit_post_blog_status_pic = False

        for key in submit_post_blog_img_provided:
            if submit_post_blog_img_provided[key] == False:
                submit_post_blog_missing_pic = True
        
        for key in submit_post_blog_img_provided:
            if submit_post_blog_img_status[key] == False:
                submit_post_blog_status_pic = True

        if submit_post_blog_missing_pic == True and submit_post_blog_status_pic == True:
            flash("Blog post submitted successfully, but one or more pictures were missing and at least one couldn't be downloaded.")
        elif submit_post_blog_missing_pic == True:
            flash("Blog post submitted successfully, but one or more pictures were missing.")
        elif submit_post_blog_status_pic == True:
            flash("Blog post submitted successfully, but one or more pictures couldn't be downloaded.")
        else:
            flash("Blog post submitted successfully!")

        # clear form:
        form.theme.data = ""
        form.date.data = datetime.now
        form.title.data = ""
        form.intro.data = ""
        form.body.data = ""
        form.picture_v.data = ""
        form.picture_v_source.data = ""
        form.picture_h.data = ""
        form.picture_h_source.data = ""
        form.picture_s.data = ""
        form.picture_s_source.data = ""
        form.picture_alt.data = ""
        form.meta_tag.data = ""
        form.title_tag.data = ""

        return redirect(url_for('account.dashboard'))

    return render_template("dashboard/posts_submit_new.html", logged_in=current_user.is_authenticated, form=form)

# POST MANGEMENT -  ADMIN
# View table with all posts and manage posts: Admin only
@dashboard.route("/dashboard/manage_posts")
@login_required
def posts_table():
    all_blog_posts_submitted = Blog_Posts.query.order_by(Blog_Posts.id)
    return render_template("dashboard/posts_table.html", logged_in=current_user.is_authenticated, all_blog_posts_submitted=all_blog_posts_submitted)

# Approve posts: only users of type admin can approve posts
# Approved posts are published on the blog
# When a post is approved, this will count towards active posts in the blog statictics.

@dashboard.route("/dashboard/manage_posts/approve_post/<int:id>", methods=["GET", "POST"])
@login_required
def approve_post(id):
    post_to_approve = Blog_Posts.query.get_or_404(id)
    if request.method == "POST":
        post_to_approve.admin_approved = "TRUE"
        try:
            db.session.commit()
            flash("This post has been admin approved.")
            update_approved_post_stats(1)
            return redirect(url_for('dashboard.posts_table'))
        except:
            flash("There was a problem approving this post.")
            return render_template("dashboard/posts_approve_post.html", logged_in=current_user.is_authenticated, post_to_approve=post_to_approve)
    else:
        return render_template("dashboard/posts_approve_post.html", logged_in=current_user.is_authenticated, post_to_approve=post_to_approve)

# Disapprove (disallow) posts: only user accounts of type admin can disapprove a post
# Disapproving a post will unpublish it from the blog
# This action will be reflected in the blog stats of active posts
@dashboard.route("/dashboard/manage_posts/disallow_post/<int:id>", methods=["GET", "POST"])
@login_required
def disallow_post(id):
    post_to_disallow = Blog_Posts.query.get_or_404(id)
    if request.method == "POST":
        post_to_disallow.admin_approved = "FALSE"
        try:
            db.session.commit()
            flash("This post is no longer admin approved.")
            update_approved_post_stats(-1)
            return redirect(url_for('dashboard.posts_table'))
        except:
            flash("There was a problem disallowing this post.")
            return render_template("dashboard/posts_disallow_post.html", logged_in=current_user.is_authenticated, post_to_disallow=post_to_disallow)
    else:
        return render_template("dashboard/posts_disallow_post.html", logged_in=current_user.is_authenticated, post_to_disallow=post_to_disallow)

# POST MANAGEMENT - AUTHORS DASH
# View table with all posts this author has submitted
@dashboard.route("/dashboard/manage_posts_author")
@login_required
def posts_table_author():
    all_blog_posts_submitted = Blog_Posts.query.filter(
        Blog_Posts.author_id == current_user.id).all()
    return render_template("dashboard/posts_table_author.html", logged_in=current_user.is_authenticated, all_blog_posts_submitted=all_blog_posts_submitted)


# POST MANGEMENT -  ADMIN AND AUTHORS
# Previewing a post
@dashboard.route("/dashboard/manage_posts_author/preview_post/<int:id>", endpoint='preview_post_author')
@dashboard.route("/dashboard/manage_posts/preview_post/<int:id>")
@login_required
def preview_post(id):
    post_to_preview = Blog_Posts.query.get_or_404(id)
    return render_template("dashboard/posts_preview_post.html", logged_in=current_user.is_authenticated, post_to_preview=post_to_preview)

# Editing a post - ADMIN AND AUTHORS
#make authors as a list
@dashboard.route("/dashboard/manage_posts_author/edit_post/<int:id>", endpoint='edit_post_author', methods=["GET", "POST"])
@dashboard.route("/dashboard/manage_posts/edit_post/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):

    # getting post information
    post_to_edit = Blog_Posts.query.get_or_404(id)
    themes_list = [(u.id, u.theme) for u in db.session.query(Blog_Theme).all()]
    form = The_Posts(obj=themes_list)
    form.theme.choices = themes_list

    # changing the post
    if form.validate_on_submit():
        # get all information from the form with the exeption of the blog post pictures
        # this will enable the saving of the information even if there is an error with the picture upload:
        post_to_edit.theme_id = form.theme.data
        post_to_edit.date_to_post = form.date.data
        post_to_edit.title = form.title.data
        post_to_edit.intro = form.intro.data
        post_to_edit.body = form.body.data
        post_to_edit.picture_v_source = form.picture_v_source.data
        post_to_edit.picture_h_source = form.picture_h_source.data
        post_to_edit.picture_s_source = form.picture_s_source.data
        post_to_edit.picture_alt = form.picture_alt.data
        post_to_edit.meta_tag = form.meta_tag.data
        post_to_edit.title_tag = form.title_tag.data

        # add form information to database without the pictures:
        try:
            db.session.commit()
        except:
            flash("Oops, error saving your changes, check all fields and try again.")
        
        # checking images: one image at a time
        the_post_id = post_to_edit.id

        submit_post_blog_img_provided = dict(v=False, h=False, s=False)
        submit_post_blog_img_status = dict(v=False, h=False, s=False)

        def submit_post_blog_img_handle(img_filename, img_format):
            accepted_img_format = ["v", "h", "s"]
            if img_format not in accepted_img_format:
                raise NameError(
                    "submit_post_blog_img_handle function was supplied an invalid img_format")
            new_img_name = check_blog_picture(
                the_post_id, img_filename, img_format)
            if new_img_name:
                new_img_format = "picture_" + img_format
                the_img = request.files[new_img_format]
                try:
                    if img_format == "v":
                        delete_blog_img(post_to_edit.picture_v)
                        post_to_edit.picture_v = new_img_name
                    elif img_format == "h":
                        delete_blog_img(post_to_edit.picture_h)
                        post_to_edit.picture_h = new_img_name
                    else:
                        delete_blog_img(post_to_edit.picture_s)
                        post_to_edit.picture_s = new_img_name
                    the_img.save(os.path.join(
                        current_app.config["BLOG_IMG_FOLDER"], new_img_name))
                    db.session.commit()
                    submit_post_blog_img_status[img_format] = True
                except:
                    submit_post_blog_img_status[img_format] = False

        img_size_not_accepted = False

        # checking picture vertical:
        if form.picture_v.data and int(form.picture_v_size.data) < 1500000:
            img_v_filename = secure_filename(form.picture_v.data.filename)
            submit_post_blog_img_handle(img_v_filename, "v")
            submit_post_blog_img_provided["v"] = True
        elif form.picture_v_size.data and int(form.picture_v_size.data) > 1500000:
            img_size_not_accepted = True
        elif form.picture_v_size.data and int(form.picture_v_size.data) < 1500000:
            submit_post_blog_img_provided["v"] = True
        else:
            submit_post_blog_img_provided["v"] = False

        # checking picture horizontal:
        if form.picture_h.data and int(form.picture_h_size.data) < 1500000:
            img_h_filename = secure_filename(form.picture_h.data.filename)
            submit_post_blog_img_handle(img_h_filename, "h")
            submit_post_blog_img_provided["h"] = True
        elif form.picture_h_size.data and int(form.picture_h_size.data) > 1500000:
            img_size_not_accepted = True
        elif form.picture_h_size.data and int(form.picture_h_size.data) < 1500000:
            submit_post_blog_img_provided["h"] = True
        else:
            submit_post_blog_img_provided["h"] = False

        # checking picture squared:
        if form.picture_s.data and int(form.picture_s_size.data) < 1500000:
            img_s_filename = secure_filename(form.picture_s.data.filename)
            submit_post_blog_img_handle(img_s_filename, "s")
            submit_post_blog_img_provided["s"] = True
        elif form.picture_s_size.data and int(form.picture_s_size.data) > 1500000:
            img_size_not_accepted = True
        elif form.picture_s_size.data and int(form.picture_s_size.data) < 1500000:
            submit_post_blog_img_provided["s"] = True
        else:
            submit_post_blog_img_provided["s"] = False

        # inform the user of the status of the post
        problem_with_img_download = False

        for key in submit_post_blog_img_provided:
            if submit_post_blog_img_provided[key] == True:
                if submit_post_blog_img_status[key] == False:
                    problem_with_img_download = True

        if img_size_not_accepted == True:
            flash("Blog post edit saved, but one or more pictures were too large and couldn't be saved.")
        elif problem_with_img_download == True:
            flash(
                "Blog post saved, but one or more pictures couldn't be saved. Check picture format.")
        else:
            flash("Blog post editted successfully!")

        if current_user.type == "admin" or current_user.type == "super_admin":
            return redirect(url_for("dashboard.posts_table", logged_in=current_user.is_authenticated))
        else:
            return redirect(url_for("dashboard.posts_table_author", logged_in=current_user.is_authenticated))
        
    # filling out the form with saved post data
    form.theme.data = post_to_edit.theme_id
    form.author.data = post_to_edit.author.name
    form.date.data = post_to_edit.date_to_post
    form.title.data = post_to_edit.title
    form.intro.data = post_to_edit.intro
    form.body.data = post_to_edit.body
    form.picture_v_source.data = post_to_edit.picture_v_source
    form.picture_h_source.data = post_to_edit.picture_h_source
    form.picture_s_source.data = post_to_edit.picture_s_source
    form.picture_alt.data = post_to_edit.picture_alt
    form.meta_tag.data = post_to_edit.meta_tag
    form.title_tag.data = post_to_edit.title_tag
    return render_template('dashboard/posts_edit_post.html', logged_in=current_user.is_authenticated, form=form, post_to_edit=post_to_edit)

# Deleting a post 
@dashboard.route("/dashboard/manage_posts_author/delete_post/<int:id>", endpoint='delete_post_author', methods=["GET", "POST"])
@dashboard.route("/dashboard/manage_posts/delete_post/<int:id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
    # get post, and its associated likes and comments
    post_to_delete = Blog_Posts.query.get_or_404(id)
    post_likes = db.session.query(Blog_Likes).filter(
        Blog_Likes.post_id == id).all()
    comments = db.session.query(Blog_Comments).filter(
        Blog_Comments.post_id == id).all()

    if request.method == "POST":
        try:
            # delete likes associated
            for like in post_likes:
                db.session.delete(like)

            # delete comments and replies associated
            for comment in comments:
                replies = Blog_Replies.query.filter_by(comment_id=comment.id).all()
                for reply in replies:
                    db.session.delete(reply)
                db.session.delete(comment)

            # delete bookmarks associated
            bookmarks = Blog_Bookmarks.query.filter_by(post_id=id).all()
            for bookmark in bookmarks:
                db.session.delete(bookmark)
            
            # delete the post and commit
            if post_to_delete.admin_approved == "TRUE":
                post_was_approved = True
            db.session.delete(post_to_delete)
            db.session.commit()

            # delete pictures associated
            delete_blog_img(post_to_delete.picture_v)
            delete_blog_img(post_to_delete.picture_h)
            delete_blog_img(post_to_delete.picture_s)

            # update stats
            if post_was_approved:
                update_approved_post_stats(-1)

            flash("Post deleted successfully.")
            if current_user.type == "author":
                return redirect(url_for('dashboard.posts_table_author'))
            else:
                return redirect(url_for('dashboard.posts_table'))
        except:
            db.session.rollback()
            flash("There was a problem deleting this post and associated data.")
            if current_user.type == "author":
                return redirect(url_for('dashboard.posts_table_author'))
            else:
                return redirect(url_for('dashboard.posts_table'))
    else:
        return render_template("dashboard/posts_delete_post.html", logged_in=current_user.is_authenticated, post_to_delete=post_to_delete, post_likes=post_likes, comments=comments)
