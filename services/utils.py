import jwt
import bcrypt
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

JWT_SECRET = os.environ.get("JWT_SECRET")
SENDER_ADDRESS = os.environ.get("SENDER_ADDRESS")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
CLIENT_URL = os.environ.get("CLIENT_URL")


def encode(user):
    return jwt.encode(
        {
            "email": user['email'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        JWT_SECRET,
        algorithm='HS256').decode("utf-8")


def decode(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithm='HS256')
    except:
        return {}


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf8'),
                         bcrypt.gensalt()).decode('utf8')


def decrypt_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf8'),
                          hashed_password.encode('utf8'))


def send_confirmation(receiver_address, checking_id):
    return send_mail(receiver_address=receiver_address,
                     subject='Auth - Confirm your account',
                     mail_content="{}/user/confirm?uniqid={}&email={}".format(
                         CLIENT_URL, checking_id, receiver_address))


def send_mail(receiver_address, subject, mail_content):
    message = MIMEMultipart()
    message['From'] = SENDER_ADDRESS
    message['To'] = receiver_address
    message['Subject'] = subject
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(SENDER_ADDRESS, SENDER_PASSWORD)
    text = message.as_string()
    session.sendmail(SENDER_ADDRESS, receiver_address, text)
    session.quit()
    print('Mail Sent')
