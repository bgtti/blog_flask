from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from app.extensions import db, login_manager
from app.models.user import Blog_User
from app.models.posts import Blog_Posts
from app.account.forms import The_Accounts
from app.account.helpers import hash_pw, allowed_imgs
from app.models.helpers import update_stats_comments_total, update_stats_users_total, pic_src_user
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash  # used in login
from werkzeug.utils import secure_filename
import uuid as uuid
import os

account = Blueprint('account', __name__)

# Pages: login, logout, signup, account
# Routes available for all registered users (all user types) + login and signup (available for all registered and non-registered users)

# LOGIN, SIGN UP, LOG OUT

@login_manager.user_loader
def load_user(user_id):
    return Blog_User.query.get(int(user_id))

@account.route("/signup", methods=["GET", "POST"])
def signup():
    # in the future, check if username is unique
    if request.method == "POST":
        if Blog_User.query.filter_by(email=request.form.get("email")).first():
            # if user already exists:
            flash("This email is already registered with us. Log-in instead!")
            return redirect(url_for("account.login"))

        new_user = Blog_User(
            name=request.form.get("username"),
            email=request.form.get("email"),
            password=hash_pw(request.form.get("password")),
            type="user"
        )
        db.session.add(new_user)
        db.session.commit()
        update_stats_users_total()

        login_user(new_user)

        return redirect(url_for('account.dashboard'))

    return render_template('account/signup.html', logged_in=current_user.is_authenticated)


@account.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        the_user = Blog_User.query.filter_by(email=email).first()
        # wrong email:
        if not the_user:
            flash("This email does not exist in our database.")
            return redirect(url_for("account.login"))
        # wrong password:
        elif not check_password_hash(the_user.password, password):
            flash("Incorrect password, please try again.")
            return redirect(url_for("account.login"))
        # user is blocked:
        elif the_user.blocked == "TRUE":
            flash("Your account has been blocked. Please contact us for more information")
            return redirect(url_for("account.login"))
        # email exists and password is correct
        else:
            login_user(the_user)
            return redirect(url_for('account.dashboard'))
    return render_template("account/login.html", logged_in=current_user.is_authenticated)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('website.home'))



# DASHBOARDs
# displaying user dashboard after log-in according to the account type: user, author, or admin
@account.route("/dashboard")
@login_required
def dashboard():
    if current_user.type == "user":
        return render_template('account/dashboard_user.html', name=current_user.name, logged_in=True)
    elif current_user.type == "author":
        posts_pending_admin = Blog_Posts.query.filter(Blog_Posts.admin_approved == "FALSE").filter(
            Blog_Posts.author_id == current_user.id).all()
        return render_template('account/dashboard_author_dash.html', name=current_user.name, logged_in=True, posts_pending_admin=posts_pending_admin)
    else:
        posts_pending_approval = Blog_Posts.query.filter_by(
            admin_approved="FALSE").all()
        return render_template('account/dashboard_admin_dash.html', name=current_user.name, logged_in=True, posts_pending_approval=posts_pending_approval)

# ***********************************************************************************************
# ACCOUNT MANAGEMENT, BOOKMARKS, HISTORY

# OWN ACCOUNT MANAGEMENT - all users
# Account information

@account.route("/dashboard/manage_account")
@login_required
def manage_acct():
    return render_template("account/account_mgmt.html", logged_in=current_user.is_authenticated)

# Account information form: moved from here

# Update account information


@account.route("/dashboard/manage_account/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_own_acct_info(id):
    form = The_Accounts()
    user_at_hand = Blog_User.query.get_or_404(id)

    if form.validate_on_submit():
        user_at_hand.name = form.username.data
        user_at_hand.email = form.email.data
        user_at_hand.about = form.about.data

        try:
            db.session.commit()
            flash("Account information updated successfully!")
            # no time for flash, change way of displaying success
            return redirect(url_for('account.manage_acct'))
        except:
            flash("Oops, error updating account information, try again.")
            return redirect(url_for('account.manage_acct'))

    # filling out the form with saved post data
    form.username.data = user_at_hand.name
    form.email.data = user_at_hand.email
    form.about.data = user_at_hand.about
    return render_template("account/account_mgmt_update.html", logged_in=current_user.is_authenticated, form=form)

# Update account information: changing the picture

@account.route("/dashboard/manage_account/update_picture/<int:id>", methods=["GET", "POST"])
@login_required
def update_own_acct_picture(id):
    form = The_Accounts()
    user_at_hand = Blog_User.query.get_or_404(id)
    if user_at_hand.picture == "" or user_at_hand.picture == pic_src_user("Picture_default.jpg"):
        profile_picture = None
    else:
        profile_picture = user_at_hand.picture

    if request.method == "POST":
        # if form.validate_on_submit():
        print(f"HERE")
        if form.picture.data:
            # get name from image file:
            pic_filename = secure_filename(form.picture.data.filename)

            # check if extension is allowed:
            if not allowed_imgs(pic_filename):
                flash("Sorry, this image extension is not allowed.")
                return redirect(url_for('account.update_own_acct_picture', id=id))

            # insert a unique id to the filename to make sure there arent two picutes with the same name:
            pic_filename_unique = str(uuid.uuid1()) + "_" + pic_filename
            user_at_hand.picture = pic_filename_unique

            # get the new image
            the_img_file = request.files['picture']
        try:
            # save the img to folder and path to user
            the_img_file.save(os.path.join(
                current_app.config["PROFILE_IMG_FOLDER"], pic_filename_unique))
            # delete the old picture from folder
            if profile_picture != None and os.path.exists(os.path.join(current_app.config["PROFILE_IMG_FOLDER"], profile_picture)):
                os.remove(os.path.join(
                    current_app.config["PROFILE_IMG_FOLDER"], profile_picture))

            db.session.commit()
            flash("Picture updated successfully!")
            # no time for flash, change way of displaying success
            return redirect(url_for('account.manage_acct'))
        except:
            flash("Oops, error updating profile picture, try again.")
            return redirect(url_for('account.manage_acct'))

    return render_template("account/account_mgmt_picture.html", logged_in=current_user.is_authenticated, form=form, profile_picture=profile_picture)


# Delete account
@account.route("/dashboard/manage_account/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_own_acct(id):
    user_at_hand = Blog_User.query.get_or_404(id)
    if request.method == "POST":
        if id == 1:
            flash("Authorization denied: this user cannot be deleted")
            return redirect(url_for('account.manage_acct'))
        else:
            try:
                db.session.delete(user_at_hand)
                db.session.commit()
                flash("Your account was deleted successfully.")
                return redirect(url_for("website.home"))
            except:
                flash("There was a problem deleting your account.")
                return redirect(url_for('account.manage_acct'))
    else:
        return render_template("account/account_mgmt_delete.html", logged_in=current_user.is_authenticated)

# BOOKMARKS

# HISTORY
