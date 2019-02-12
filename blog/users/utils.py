import os
import secrets

from flask import current_app, url_for
from PIL import Image

from blog import mail
from flask_mail import Message


def save_icon(account_icon):
    file_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(account_icon.filename)
    file_name = file_hex + file_ext
    file_path = os.path.join(current_app.root_path, "static", "account_icons", file_name)

    output_size = (125, 125)
    final_icon = Image.open(account_icon)
    final_icon.thumbnail(output_size)
    final_icon.save(file_path)

    return file_name


def send_reset_password_email(user):
    token = user.get_reset_token()
    message = Message(
        "Flask Blog Password Reset Request", sender="noreply@flaskblog.com", recipients=[user.email]
    )
    message.body = f"To reset your password, vist the following link:\n{url_for('users.reset_password_token', token=token, _external=True)}.\nIf this was not you, ignore this message."
    mail.send(message)
