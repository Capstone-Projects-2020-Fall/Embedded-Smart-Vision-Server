from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtfroms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from .models import User

class ResetPasswordRequestForm(FlaskForm):
	email = StringField(('Email'), validators = [DataRequired(), Email()]
	submit = SubmitField(('Request Password Reset'))
	
class ResetPasswordForm(FlaskForm):
	password = PasswordField(('New Password'), validators = [DataRequired()])
	password2 = PasswordField(('Confirm New Password'), validators=[DataRequired(), EqualTo(password)])
	submit = SubmitField(('Request Password Reset'))
