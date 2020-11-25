from flask import Blueprint, redirect, url_for
from flask_login import login_user, logout_user, login_required



user_logout = Blueprint('user_logout', __name__, template_folder="templates")



@user_logout.route('/userlogout')
@login_required
def show_user_logout():
	logout_user()
	return redirect(url_for('user_logout.show_user_logout_confirmation'))

@user_logout.route('/userlogout')
def show_user_logout_confirmation():
    return render_template('user_logout.html', current_page='user_logout')