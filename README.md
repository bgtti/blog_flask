# blog_flask
A responsive travel blog template created using python flask and bootstrap.

![Preview of app](Blog_Preview.png)

![Preview of app](Blog_Preview_Posts.png)

![Preview of app](Blog_Preview_Responsive.png)

## Contact form email
If you are using this code, create a .env file to the main folder, with the following variables:
EMAIL_ADDRESS = "..." <-- replace "..." with your gmail address
EMAIL_PASSWORD = "..." <-- replace "..." with your gmail app password (two-step verification needed)

The email address and password will be used to receive messages sent through the contact form.
The credentials (email address and password) have been saved to an .env file, and the variables imported into main.py. This information must be replaced for the code to work on local by anyone willing to use the codebase.
Messages sent though the contact form are sent and received by a gmail account. If another provider is used, replace "smtp.gmail.com" with the information from the other provider.

## Database
Messages received through the contact form are stored in an SQLite database.

## Log in
Validation using WTforms

## Requirements
The required dependencies are stored in requirements.txt.
pip freeze > requirements.txt will output a list of all installed Python modules with their versions, shall you make changes to the project.
Use pip install -r requirements.txt to install all the modules.