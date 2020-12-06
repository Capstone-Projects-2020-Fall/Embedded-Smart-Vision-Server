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
    two_factor_enabled = db.Column(db.Boolean, default=False, nullable=False)