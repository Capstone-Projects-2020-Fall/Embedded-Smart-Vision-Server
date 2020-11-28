from flask import render_template, redirect, url_for, request, session, Blueprint
from flask_login import login_user, login_required, current_user
from application.Blueprints.User2FA.form_2fa import Enable2faForm, Confirm2faForm, Disable2faForm
from .models import User
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
    
    session['phone'] = verification_phone
    request_verification_token(session['phone'])
    
    return redirect(url_for('user2fa.verify_2fa'))

@user2fa.route('/verify2fa')
def verify_2fa():
    return render_template('verify_2fa.html', current_page = 'verify_2fa')

@user2fa.route('/verify2fa', methods=['POST'])
def verify_2fa_post():
    token = request.form.get('verificationcode')
    
    if check_verification_token(phone, token):
        del session['phone']
        if current_user.is_authenticated:
            current_user.verification_phone = phone
            db.session.commit()
            flash('Two-factor authentication is now enabled')
            return redirect(url_for('user_profile.show_user_profile'))
        else:
            username: session['username']
            del session['username']
            user = User.query.filter_by(username = username).first()
            login_user(user, remember = remember)
            return redirect(url_for('user_profile.show_user_profile'))

@user2fa.route('/disable_2fa')
@login_required
def disable_2fa():
    return render_template('disable_2fa.html', current_page = 'disable_2fa')

@user2fa.route('/disable_2fa', methods=['POST'])
@login_required
def disable_2fa_post():
    current_user.verification_phone = None
    db.session.commit()
    flash('Two-factor authentication is now disabled.')
    return redirect(url_for('user_profile.show_user_profile'))
