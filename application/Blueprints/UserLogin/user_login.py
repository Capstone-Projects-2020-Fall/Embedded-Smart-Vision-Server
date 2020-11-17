from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from application import db
from flask_login import login_user
from application.Blueprints.User2FA.twilio_verify import request_verification_token


user_login = Blueprint('user_login', __name__, template_folder='templates')


@user_login.route('/userlogin')
def show_user_login():
	return render_template('user_login.html', current_page='user_login')

@user_login.route('/userlogin', methods=['GET', 'POST'])
def show_user_login_post():
	email = request.form.get('email')
	username = request.form.get('username')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(email=email).first()

	if not user or not check_password_hash(user.password, password):
		flash('Please check your login details and try again.')
		return redirect(url_for('user_login.show_user_login'))

	if user.two_factor_enabled():
		request_verification_token(user.verification_phone)
		session['username'] = user.username
		session['phone'] = user.verification_phone
		return redirect(url_for('user2fa.verify_2fa', next = next_page, remember = '1' if form.remember_me.data else '0'))

	login_user(user, remember=remember)
	return redirect(url_for('user_profile.show_user_profile', user = user))
