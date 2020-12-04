from flask_wtf import FlaskForm
import phonenumbers
from .models import User
from wtforms import SubmitField, StringField
from wtforms.validators import ValidationError, DataRequired

class Enable2faForm(FlaskForm):
    verification_phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Enable 2FA')

    def validate_verification_phone(self, verification_phone):
        try:
            p = phonenumbers.parse(verification_phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumbersutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class Confirm2faForm(FlaskForm):
    token = StringField('Token')
    submit = SubmitField('Verify')

class Disable2faForm(FlaskForm):
    submit = SubmitField('Disable 2FA')
