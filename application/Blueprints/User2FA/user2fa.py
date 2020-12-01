from flask import render_template, redirect, url_for, request, session, Blueprint
from flask_login import login_user, login_required, current_user
from application.Blueprints.User2FA.form_2fa import Enable2faForm, Confirm2faForm, Disable2faForm
from application.models import User
from application.Blueprints.User2FA.twilio_verify import request_verification_token, check_verification_token
from application import db

user2fa = Blueprint('user2fa', __name__, template_folder='templates')

@user2fa.route('/enable_2fa')
@login_required
def enable_2fa():
    return render_template('enable_2fa.html', current_page = 'enable_2fa')

@user2fa.route('/enable_2fa', methods=['POST'])
@login_required
def enable_2fa_post():
    verification_phone = request.form.get('cellphonenumber')
    
    code = request.form.get('token')
    verify_code = request.form.get('verifytoken')
    
    email = request.form.get('email')
    
    # session['phone'] = verification_phone
    phone = verification_phone
    
    if code == verify_code:
        # session['code'] = code
        code = code
    
    print('Cell Phone Number: {}'.format(phone))
    print('Code: {}'.format(code))
    
    user = User.query.filter_by(email=email).first()
    user.verification_phone = phone
    user.token = code
    user.two_factor_enabled = True
    db.session.commit()
    
    print("current user: id = {}, password = {}, email = {}, name = {}, verification_phone = {}, token = {}".format(user.id, user.password, user.email, user.name, user.verification_phone, user.token))
    print(user.two_factor_enabled)
    
    return redirect(url_for('user_profile.show_user_profile'))

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
    
    return redirect(url_for('user_profile.show_user_profile'))

@user2fa.route('/disable_2fa')
@login_required
def disable_2fa():
    return render_template('disable_2fa.html', current_page = 'disable_2fa')

@user2fa.route('/disable_2fa', methods=['POST'])
@login_required
def disable_2fa_post():
    email = request.form.get('email')
    
    user = User.query.filter_by(email=email).first()
    
    print("Before disabling of 2-factor authentication: ")
    print("id  = {}, password = {}, email = {}, name = {}, verification_phone = {}".format(user.id, user.password, user.email, user.name, user.verification_phone))
    user.verification_phone = None
    user.token = ''
    user.two_factor_enabled = False
    db.session.commit()
    print('Two-factor authentication is now disabled.')
    print("After disabling of 2-factor authentication: ")
    print("id  = {}, token = {}, password = {}, email = {}, name = {}, verification_phone = {}".format(user.id, user.token, user.password, user.email, user.name, user.verification_phone))
    return redirect(url_for('user_profile.show_user_profile'))
