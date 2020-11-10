from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from application import db
from flask_login import login_user


user_login = Blueprint('user_login', __name__, template_folder='templates')


@user_login.route('/userlogin')
def show_user_login():
	return render_template('user_login.html', current_page='user_login')

@user_login.route('/userlogin', methods=['POST'])
def show_user_login_post():
	email = request.form.get('email')
	username = request.form.get('username')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(email=email).first()

	if not user or not check_password_hash(user.password, password):
		flash('Please check your login details and try again.')
		return redirect(url_for('user_login.show_user_login'))

	login_user(user, remember=remember)
	return redirect(url_for('user_profile.show_user_profile'))
