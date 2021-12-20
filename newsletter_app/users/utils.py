from flask import render_template, url_for, flash, redirect
from flask_login import current_user
from flask_mail import Message
from newsletter_app import db, bcrypt, mail
from newsletter_app.models import User


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@email-newsletter-generator.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, reset the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)
