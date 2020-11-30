from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, login_required
from flask_babel import _
from application import db
from application.Blueprints.UserResetPassword.forms import ResetPasswordRequestForm, ResetPasswordForm
from .models import User
from application.Blueprints.UserResetPassword.email import send_password_reset_email
from application.Blueprints.UserResetPassword.twilio_verify import request_verification_token, check_verification_token
from werkzeug.security import generate_password_hash, check_password_hash

user_reset_password = Blueprint('user_reset_password', __name__, template_folder='templates')

@user_reset_password.route('/reset_password_form')
def reset_password_form():
    return render_template('reset_password_form.html', current_page='reset_password_form')

@user_reset_password.route('/reset_password_form', methods=['POST'])
def reset_password_form_post():
    email = request.form.get('email')
    username = request.form.get('username')
    name = request.form.get('name')
    new_password = request.form.get('newpassword')
    confirm_new_password = request.form.get('confirmnewpassword')
    
    user = User.query.filter_by(email=email).first()
    
    print("Before reseting the password: ")
    print("id  = {}, password = {}, email = {}, name = {}".format(user.id, user.password, user.email, user.name))
    
    print("Before setting the value for password to an empty string: ")
    print("id  = {}, password = {}, email = {}, name = {}".format(user.id, user.password, user.email, user.name))
    user.password = ''
    print("After setting the value for password to an empty string: ")
    print("id  = {}, password = {}, email = {}, name = {}".format(user.id, user.password, user.email, user.name))
    new_password = generate_password_hash(new_password, method='sha256')
    user.password = new_password
    db.session.commit()
    print("After reseting the password: ")
    print("id  = {}, password = {}, email = {}, name = {}".format(user.id, user.password, user.email, user.name))
    return redirect(url_for('user_login.show_user_login'))
