from flask import Blueprint, render_template


user_profile = Blueprint('user_profile', __name__, template_folder='templates')


@user_profile.route('/userprofile')
def show_user_profile():
	return render_template('user_profile.html', current_page='user_profile')
