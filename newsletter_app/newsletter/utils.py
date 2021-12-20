from flask import render_template
from flask_mail import Message
from newsletter_app import mail


def send_newsletter_email(newsletter, articles, subject, to, cc, bcc):
    msg = Message(subject=subject,
                  sender='noreply@newsletter-generator.com',
                  recipients=to,
                  cc=cc,
                  bcc=bcc)
    msg.html = render_template('preview.html', newsletter=newsletter, articles=articles, sending_mail=True)
    mail.send(msg)
