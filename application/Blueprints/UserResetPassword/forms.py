from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtfroms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_bebel import _, lazy_gettext as -l
from .models import User

class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('Email'), validators = [DataRequired(), Email()]
	submit = SubmitField(_l('Request Password Reset'))
	
class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('New Password'), validators = [DataRequired()])
	password2 = PasswordField(_l('Confirm New Password'), validators=[DataRequired(), EqualTo(password)])
	submit = SubmitField(_l('Request Password Reset'))
