from flask import render_template, redirect, url_for, request, session, Blueprint
from flask_login import login_user, login_required, current_user
from application.Blueprints.User2FA.form_2fa import Enable2faForm, Confirm2faForm, Disable2faForm
from .models import User
from application.Blueprints.User2FA.twilio_verify import request_verification_token, check_verification_token
from application import db

user2fa = Blueprint('user2fa', __name__, template_folder='templates')

@user2fa.route('/enable_2fa', methods=['GET', 'POST'])
@login_required
def enable_2fa():
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('user2fa.verify_2fa'))
    return render_template('enable_2fa.html', form = form, current_page = 'enable_2fa')

@user2fa.route('/verify2fa', methods=['GET', 'POST'])
def verify_2fa():
    form = Confirm2faForm()
    if check_verification_token(phone, form.token.data):
        del session['phone']
        if current_user.is_authenticated:
            current_user.verification_phone = phone
            db.session.commit()
            flash('Two-factor authentication is now enabled')
            return redirect(url_for('user_profile.show_user_profile'))
        else:
            username: session['username']
            del session['username']
            user = User.query.filter_by(username=username).first()
            next_page = request.args.get('next')
            remember = request.args.get('remember', '0') == '1'
            login_user(user, remember=remember)
            return redirect(next_page)
        form.token.errors.append('Invalid token')
    return render_template('verify_2fa.html', form = form, current_page = 'verify_2fa')

@user2fa.route('/disable_2fa', methods=['GET', 'POST'])
@login_required
def disable_2fa():
    form = Disable2faForm()
    if form.validate_on_submit():
        current_user.verification_phone = None
        db.session.commit()
        flash('Two-factor authentication is now disabled.')
        return redirect(url_for(user_profile.show_user_profile))
    return render_template('disable_2fa.html', form = form, current_page = 'disable_2fa')

