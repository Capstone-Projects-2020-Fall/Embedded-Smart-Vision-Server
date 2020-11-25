from flask import render_template, current_app
from flask_babel import _
from application.Blueprints.UserResetPassword.send_email import send_email

def send_password_reset_email(user):
	token = user.get_reset_password_token()
	send_email(_('[EmbeddedSmartVision] Reset Your Password'), sender = current_app.config['ADMINS'][0], recepients = [user.email], text_body = render_template('templates/reset_password.txt', user = user, token = token), html_body = render_template('templates/reset_password.html', user = user, token = token))