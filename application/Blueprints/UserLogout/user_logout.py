from flask import Blueprint, redirect, url_for
from flask_login import login_user, logout_user, login_required



user_logout = Blueprint('user_logout', __name__)



@user_logout.route('/userlogout')
@login_required
def show_user_logout():
	logout_user()
	return redirect(url_for('user_login.show_user_login'))
