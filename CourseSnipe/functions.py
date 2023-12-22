from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl, smtplib, os, email.utils

load_dotenv()

def send_email(message):
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_receiver = '@gmail.com'

    subject = 'You Got Your Course!'
    body = message

    em = EmailMessage()
    em["From"] = email.utils.formataddr(('RemPy', email_sender))
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

