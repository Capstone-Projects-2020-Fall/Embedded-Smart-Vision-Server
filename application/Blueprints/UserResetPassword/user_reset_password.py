from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, login_required
from flask_babel import _
from application import db
from application.Blueprints.UserResetPassword.forms import ResetPasswordRequestForm, ResetPasswordForm
from .models import User
from application.Blueprints.UserResetPassword.email import send_password_reset_email
from application.Blueprints.UserResetPassword.twilio_verify import request_verification_token, check_verification_token

user_reset_password = Blueprint('user_reset_password', __name__, template_folder='templates')

@user_reset_password.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('user_login.show_user_login'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash(_('Check your email for the instructions to reset your password'))
		return redirect(url_for(user_login.show_user_login))
	return render_template('reset_password_request.html', title = _('Reset Password'), form = form)
	
@user_reset_password.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('user_login.show_user_login'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('user_login.show_user.login'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash(_('Your password has been reset.'))
		return redirect(url_for('user_login.show_user_login'))
	return render_template('reset_password_form.html', form = form)
