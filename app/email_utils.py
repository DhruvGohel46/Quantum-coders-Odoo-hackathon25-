# app/email_utils.py
from flask_mail import Message
from app import mail
from flask import current_app
import threading

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    
    thread = threading.Thread(target=send_async_email, args=(current_app, msg))
    thread.start()

def send_swap_request_email(user, item, requester):
    subject = f"New Swap Request for {item.title}"
    sender = current_app.config['MAIL_USERNAME']
    recipients = [user.email]
    text_body = f"""
    Hi {user.username},

    {requester.username} has sent you a swap request for your item "{item.title}".

    Login to ReWear to view the details and respond to the request.

    Best regards,
    The ReWear Team
    """
    send_email(subject, sender, recipients, text_body)