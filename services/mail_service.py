from flask_mail import Mail, Message

from flask import current_app, render_template

from utils.singleton import Singleton


class MailService(Singleton):
    def __init__(self):
        self.mail = Mail(current_app)

    def send_mail(self, to, subject, text):
        msg = Message(subject, sender="karol.boreck@outlook.com", recipients=[to])
        msg.body = text
        self.mail.send(msg)

    def send_password_restore_mail(self, to, link):
        msg = Message(
            "Password restore", sender="karol.boreck@outlook.com", recipients=[to]
        )
        msg.html = render_template("password_restore/mail.html", link=link)
        self.mail.send(msg)
