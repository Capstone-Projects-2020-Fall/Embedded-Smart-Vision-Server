from flask import render_template, redirect, url_for, request, session, Blueprint
from flask_login import login_user, login_required, current_user
from application.Blueprints.User2FA.form_2fa import Enable2faForm, Confirm2faForm, Disable2faForm
from application.models import User
from application.Blueprints.User2FA.twilio_verify import request_verification_token, check_verification_token
from application import db

user2fa = Blueprint('user2fa', __name__, template_folder='templates')

@user2fa.route('/enable_2fa')
def enable_2fa():
    return render_template('enable_2fa.html', current_page = 'enable_2fa')

@user2fa.route('/enable_2fa', methods=['POST'])
def enable_2fa_post():
    verification_phone = request.form.get('cellphonenumber')
    code = request.form.get('token')
    email = request.form.get('email')
    phone = verification_phone
    user = User.query.filter_by(email=email).first()
    print(user.email)
    user.verification_phone = phone
    user.token = code
    user.two_factor_enabled = True
    db.session.commit()
    print('Worked!!!')
    return redirect(url_for('user_login.show_user_login'))

@user2fa.route('/login_verify_2fa')
def login_verify_2fa():
    return render_template('login_verify_2fa.html', current_page = 'login_verify_2fa')

@user2fa.route('/login_verify_2fa', methods=['POST'])
def login_verify_2fa_post():
    login_code = request.form.get('logintoken')
    email = request.form.get('email')
    
    login_code = login_code
    
    user = User.query.filter_by(email=email).first()
    
    code = user.token
    
    print('login code: {}, code: {}'.format(login_code, code))
        
    if login_code != code:
        return redirect(url_for('user2fa.login_verify_2fa'))
    else: 
        return redirect(url_for('user_profile.show_user_profile'))

@user2fa.route('/disable_2fa')
def disable_2fa():
    return render_template('disable_2fa.html', current_page = 'disable_2fa')

@user2fa.route('/disable_2fa', methods=['POST'])
def disable_2fa_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    user.verification_phone = None
    user.token = None
    user.two_factor_enabled = False
    db.session.commit()
    print('verification_phone: {}, token: {}, two_factor_enabled: {}'.format(user.verification_phone, user.token, user.two_factor_enabled))
    return redirect(url_for('user_login.show_user_login'))
