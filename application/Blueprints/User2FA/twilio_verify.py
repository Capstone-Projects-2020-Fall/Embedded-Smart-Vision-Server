from flask import current_app
from twilio.rest import Client, TwilioException

def request_verification_token(phone):
    client = Client(current_app.config['TWILIO_ACCOUNT_SID'],
                    current_app.config['TWILIO_AUTH_TOKEN']).verify.services(
                        current_app.config['TWILIO_VERIFY_SERVICE_SID'])
    verify = client
    try:
        verify.verifications.create(to = phone, channel = 'sms')
    except TwilioException:
        verify.verifications.create(to = phone, channel = 'call')

def check_verification_token(phone, token):
    client = Client(current_app.config['TWILIO_ACCOUNT_SID'],
                    current_app.config['TWILIO_AUTH_TOKEN']).verify.services(
                        current_app.config['TWILIO_VERIFY_SERVICE_SID'])
    verify = client
    try:
        result = verify.verification_checks.create(to=phone, code=token)
    except TwilioException:
        return False
    return result.status == 'approved'
