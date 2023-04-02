# blog_flask
A responsive travel blog template with admin section created using python flask and bootstrap.
The blog pages 'Home', 'All Posts', 'About', and 'Contact' can be viewed by any person accessing the website, while it also contains a log-in and sign-up section, where users can create an account to like and bookmark posts, as well as use the comment section. An admin and author dashboards is also available, where posts and users can be added, editted, and deleted. 


![Preview of app](app/static/Pictures_Blog_Preview/Preview_01.png)

![Preview of app](app/static/Pictures_Blog_Preview/Preview_02.png)

![Preview of app](app/static/Pictures_Blog_Preview/Preview_03.png)

## About this project
This project is composed of a blog and blog management interface which allow for multiple user classes.
The project was written in python flask (using Blueprints), using SQLite as the database (with the help of SQLalchemy), and uses bootstrap and CSS for styling.
JavaScript was only used when necessary: to determine sizes of images prior to upload, and to allow for comments, bookmarking, and liking posts, as well as alert message display without re-loading the page for a better user experience.

### User classes
There are 5 types of user classes (implicit and explicit):
**Visitors:** webside visitors or logged out users can view the following pages: 'Home', 'All Posts', 'About', and 'Contact'. A visitor can also create an account (which will automatically create a user of type 'user'), and a logged-out user can sign in.
**User:** a logged-in user of type 'user' can bookmark or like posts. The user can also comment and reply to comments in blog posts. The user can edit his/her username, email, picture, and 'about' section.
**Author:** authors can do the same things as users of type 'user', as well as add posts, edit posts, and delete posts.
**Admin:** admins can do the same things as users of type 'user', as well as:
 - block, delete, and edit any users' and authors' accounts,
 - change a user's type from 'user' to 'author' and vice-versa,
 - approve, disapprove, and edit blog posts.
**Super-Admin:** there is only one super-admin account. Supera-admins can do everything an admin user can do, as well as managing admin-type accounts as well.

### Contact
Messages sent through the blog's 'contact' page are received by a gmail account. 
Messages received through the contact form are also stored in an SQLite database.

### Log in validation
Validation uses WTforms

### How the code is organized
The blog_flask folder contains:
- 'app' folder: where the code is
- '.env' file: with sensitive information such as the email address and password used to receive email from the contact form. Can't be downloaded, so instructions how to create it can be found in the setup section bellow.
- '.gitignore': which is used to inform git about files that shouldn't be uploaded to the git repository, such as the .env file. Can't be downloaded, so instructions how to create it can be found in the setup section bellow.
- 'create_db.py': the file used to use the db models to create the database. It is also used to create the 'Super-Admin' user, which is necessary in order to allow for the creation of 'admin' and 'author' accounts. It also sets up dummy user accounts which can be used for testing, and the blog posts, blog themes and dummy comments, likes and bookmarks.
- 'requirements.txt': stores the required dependencies for this project.
- 'run.py': used to create the app, initiate the database, and populate the database using the 'create_db.py' file.

Once you run 'run.py', the database will be initiated and an 'instance' folder will be created as well.

The routes were separated into four base folders inside the 'app' folder: website, account, dashboard, and error_handlers. The reason for this was to create a better separation of concerns by dividing the routes according to user access through Blueprints, to avoid one huge .py file and make navigating the code an easier task. We shall explore the 'app' folder next in more detail.

In the 'app' folder, you will find the following:
- 'account' folder: contains 'routes.py' which are all the routes that can be accessed by a logged-in user (routes to the log-in, sign-up, and log-out pages, dashboard, account management page, etc), as well as 'helpers.py' containing helpful functions such as hashing a password and checking if an image expension is allowed, and 'forms.py' used for a Flask Form Class.
- 'dashboard' folder: contains 'routes.py' which contains routes that can be accessed by 'admin' and 'author' type users (routes for user account and post management pages), as well as a 'forms.py' used for a Flask Form Class.
- 'dummie_data' folder: contains files with lists of information about authors, comments, posts, and themes which are used by 'create_db.py' to add the information in these files to insert information to the database when the project is first run. The data will be used to create dummie users, comments, posts, and themes that are necessary to first preview the blog. 
- 'error_handlers' folder: contains 'routes.py' which render the 404 and 500 error pages.
- 'models' folder: contains multiple files which are database models necessary to instanciate the database.
- 'static' folder: contains the CSS and JS files, as well as folders containing pictures used in blog posts and user profiles.
- 'templates' folder: contains the html files. 'base.html' is used to extend all other files. Besides 'base.html', '404.html' and '500.html', all other html files are placed into three folders ('account', 'dashboard', and 'website'), according to the Blueprint names (where you will find the routes).
- 'website' folder: contains 'routes.py' which has the routes to website pages which visiting users can access (such as the home page, 'All Posts', 'About', and 'Contact').
- '\__init__.py': used to mark a directory and indicate that is is a package. This file registers the Blueprints, for instance.
- 'config.py': stores key value pairs that can be read or accessed in the code.
- 'extensions.py': used to define and organize extensions. It is used to register the SQLAlchemy, CKEditor, and LoginManager extensions with the Flask app instance app, allowing them to be used throughout the application.

## Installation: how to use this project
Anyone is welcome to use this code (please see the liability clause at the end of this file). 
A couple of steps are needed for you to be able to run it properly:

1. install the required dependencies
2. create an .env file
3. create a .gitignore file
4. open run.py to run the code

### Step 1: installing the dependencies
When you open the folder with your code editor, you will find the requirements.txt file.
Use the pip install -r requirements.txt command to install all the modules.
If you make changes to the project you can update the requirements.txt or create a new requirements.txt file with the command pip freeze > requirements.txt . This will output a list of all installed Python modules with their versions.
Example:
Python 3.x
Flask
Jinja2

### Step 2: create a .env file
Create a .env file inside the blog_flask folder.
You should add the following variables:

EMAIL_ADDRESS = "..." <-- replace "..." with your gmail address
EMAIL_PASSWORD = "..." <-- replace "..." with your gmail app password (two-step verification needed)
SUPER_ADMIN_PASSWORD = "..." <-- replace "..." with any password of your choice which you would like to use to log in with the Super Admin account. 

The email address and password will be used to receive messages sent through the contact form.
The credentials (email address and password) have been saved to an .env file, and the variables imported into app>website>contact.py, which containes a helper function, which is then used in app>website>routes.py. This information must be replaced for the code to work on local by anyone willing to use the codebase.
Messages sent though the contact form are sent and received by a gmail account. If another provider is used, replace "smtp.gmail.com" with the information from the other provider in app>website>contact.py.
At the time of writing, Gmail allowed users to create an app password to send emails from python. You can google ' Sign in with App Passwords - Gmail Help' to learn how to create one (or follow this link: https://support.google.com/mail/answer/185833?hl=en).

The SUPER_ADMIN_PASSWORD is so that you can log into the blog using the "super@admin" dummie email. The email can be changed by managing this account, or in the 'create_db.py' file before running the app for the first time.

### Step 3: create a .gitignore file
Create a .gitignore file inside the blog_flask folder.
You should add the following to it:

instance/

.env

\__pycache__/


Alternatively, you may also find online a better and more complete template to use.

### Step 4: run the app
You can run the run.py file and open it using local host. 
That's it, you have installed the project and are ready to use the code!

## Important information and liability
This is a personal project completed by the author, which you are welcome to use and modify at your discretion.
The author, owners and maintainers of this project are not liable for any damages or losses caused by the use of this project. Use this project at your own risk. The owners and maintainers of this project do not provide any warranties or guarantees regarding the reliability, accuracy, or completeness of this project. By using this project, you agree to hold harmless the owners and maintainers of this project from any liability, damages, or losses that may arise from the use of this project.
