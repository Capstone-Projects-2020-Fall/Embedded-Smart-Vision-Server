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
    
    if current_user.is_authenticated:
        return redirect(url_for('user_login.show_user_login'))
    
    if not user:
        return redirect(url_for('user_login.show_user_login'))
    
    if new_password == confirm_new_password:
        user = User.query.filter_by(email=email).first()
        user.password = new_password
        db.session.commit()
    
    return redirect(url_for('user_login.show_user_login'))
