from flask_login import UserMixin
from . import db
from time import time
from flask import current_app
import jwt

class Video(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(100), unique=True, nullable=False)


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	videoID = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
	classification = db.Column(db.String(100), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    verification_phone = db.Column(db.String(16))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    
    def two_factor_enabled(self):
        return self.verification_phone is not None
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)        