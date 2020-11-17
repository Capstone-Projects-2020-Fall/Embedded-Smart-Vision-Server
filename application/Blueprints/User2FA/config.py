import os

class Config(object):
	TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
	TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_ACCOUNT_TOKEN')
	TWILIO_VERIFY_SERVICE_SID = os.environ.get('TWILIO_VERIFY_SERVICE_SID')

