import os  # getting .env variables
from dotenv import load_dotenv  # getting .env variables
import smtplib

# Email the Blog owner receives whenever a user sends a message through the contact form

load_dotenv()  # used to get .env variables, where username and password for the email account are stored
EMAIL = os.getenv('EMAIL_ADDRESS')# put your email here, used for the sender and receiver
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
