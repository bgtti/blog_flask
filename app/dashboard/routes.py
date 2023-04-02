from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.extensions import db
from app.models.user import Blog_User
from app.models.posts import Blog_Posts
from app.dashboard.forms import The_Posts
from app.models.themes import Blog_Theme
from datetime import datetime
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__)

# Pages: dashboard, etc
# Routes available for all registered users of types admin and author


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
    print(current_user.picture)
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
            user_to_update.name = request.form.get("username_update")
            user_to_update.email = request.form.get("email_update")
            user_to_update.type = request.form.get("accttype_update")
            user_to_update.blocked = request.form.get("acctblocked_update")
            try:
                db.session.commit()
                flash("User updated successfully!")
                # no time for flash, change way of displaying success
                return redirect(url_for('dashboard.users_table'))
            except:
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
                db.session.delete(user_to_delete)
                db.session.commit()
                flash("User deleted successfully.")
                return redirect(url_for('dashboard.users_table'))
            except:
                flash("There was a problem deleting this user.")
                return render_template("dashboard/users_user_delete.html", logged_in=current_user.is_authenticated, user_to_delete=user_to_delete)
    else:
        return render_template("dashboard/users_user_delete.html", logged_in=current_user.is_authenticated, user_to_delete=user_to_delete)

# Blocking user


@dashboard.route("/dashboard/manage_users/block/<int:id>", methods=["GET", "POST"])
@login_required
def user_block(id):
    user_to_block = Blog_User.query.get_or_404(id)
    if request.method == "POST":
        if id == 1:
            flash("Authorization error: this user cannot be blocked")
        else:
            user_to_block.blocked = "TRUE"
            try:
                db.session.commit()
                flash("User blocked successfully.")
                return redirect(url_for('dashboard.users_table'))
            except:
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

# Blog posts form: moved from here



# POST MANGEMENT -  AUTHORS
# Adding a new blog post: Authors only


@dashboard.route("/dashboard/submit_new_post", methods=["GET", "POST"])
@login_required
def submit_post():
    themes_list = [(u.id, u.theme) for u in db.session.query(Blog_Theme).all()]
    form = The_Posts(obj=themes_list)
    form.theme.choices = themes_list
    if form.validate_on_submit():
        author = current_user.id
        post = Blog_Posts(theme_id=form.theme.data,
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
        form.picture_v_source.data = ""
        form.picture_h.data = ""
        form.picture_h_source.data = ""
        form.picture_s.data = ""
        form.picture_s_source.data = ""
        form.picture_alt.data = ""
        form.meta_tag.data = ""
        form.title_tag.data = ""
        # add to database:
        db.session.add(post)
        db.session.commit()

        flash("Blog post submitted sucessfully!")

    return render_template("dashboard/posts_submit_new.html", logged_in=current_user.is_authenticated, form=form)

# POST MANGEMENT -  ADMIN
# View table with all posts and manage posts: Admin only


@dashboard.route("/dashboard/manage_posts")
@login_required
def posts_table():
    all_blog_posts_submitted = Blog_Posts.query.order_by(Blog_Posts.id)
    return render_template("dashboard/posts_table.html", logged_in=current_user.is_authenticated, all_blog_posts_submitted=all_blog_posts_submitted)

# Approve posts: Admin only


@dashboard.route("/dashboard/manage_posts/approve_post/<int:id>", methods=["GET", "POST"])
@login_required
def approve_post(id):
    post_to_approve = Blog_Posts.query.get_or_404(id)
    if request.method == "POST":
        post_to_approve.admin_approved = "TRUE"
        try:
            db.session.commit()
            flash("This post has been admin approved.")
            return redirect(url_for('dashboard.posts_table'))
        except:
            flash("There was a problem approving this post.")
            return render_template("dashboard/posts_approve_post.html", logged_in=current_user.is_authenticated, post_to_approve=post_to_approve)
    else:
        return render_template("dashboard/posts_approve_post.html", logged_in=current_user.is_authenticated, post_to_approve=post_to_approve)

# Disapprove (disallow) posts: Admin only


@dashboard.route("/dashboard/manage_posts/disallow_post/<int:id>", methods=["GET", "POST"])
@login_required
def disallow_post(id):
    post_to_disallow = Blog_Posts.query.get_or_404(id)
    if request.method == "POST":
        post_to_disallow.admin_approved = "FALSE"
        try:
            db.session.commit()
            flash("This post is no longer admin approved.")
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

# Editing a post --- MAKE AUTHORS AS A LIST


@dashboard.route("/dashboard/manage_posts_author/edit_post/<int:id>", endpoint='edit_post_author', methods=["GET", "POST"])
@dashboard.route("/dashboard/manage_posts/edit_post/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post_to_edit = Blog_Posts.query.get_or_404(id)
    themes_list = [(u.id, u.theme) for u in db.session.query(Blog_Theme).all()]
    form = The_Posts(obj=themes_list)
    form.theme.choices = themes_list
    # changing the post
    if form.validate_on_submit():
        post_to_edit.theme_id = form.theme.data
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
        # db.session.add(post_to_edit)
        db.session.commit()
        flash("Post has been updated successfully!")
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
    form.picture_v.data = post_to_edit.picture_v
    form.picture_v_source.data = post_to_edit.picture_v_source
    form.picture_h.data = post_to_edit.picture_h
    form.picture_h_source.data = post_to_edit.picture_h_source
    form.picture_s.data = post_to_edit.picture_s
    form.picture_s_source.data = post_to_edit.picture_s_source
    form.picture_alt.data = post_to_edit.picture_alt
    form.meta_tag.data = post_to_edit.meta_tag
    form.title_tag.data = post_to_edit.title_tag
    return render_template('dashboard/posts_edit_post.html', logged_in=current_user.is_authenticated, form=form)

# Deleting a post (PENDING ADAPTATION FOR AUTHORS)


@dashboard.route("/dashboard/manage_posts_author/delete_post/<int:id>", endpoint='delete_post_author', methods=["GET", "POST"])
@dashboard.route("/dashboard/manage_posts/delete_post/<int:id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
    post_to_delete = Blog_Posts.query.get_or_404(id)
    if request.method == "POST":
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post deleted successfully.")
            if current_user.type == "author":
                return redirect(url_for('dashboard.posts_table_author'))
            else:
                return redirect(url_for('dashboard.posts_table'))
        except:
            flash("There was a problem deleting this post.")
            return render_template("dashboard/posts_delete_post.html", logged_in=current_user.is_authenticated, post_to_delete=post_to_delete)
    else:
        return render_template("dashboard/posts_delete_post.html", logged_in=current_user.is_authenticated, post_to_delete=post_to_delete)
