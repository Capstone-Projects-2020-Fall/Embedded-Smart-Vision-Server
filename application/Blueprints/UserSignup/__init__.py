from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from application.VideoStream.VideoFeed import VideoStream

from flask_login import LoginManager

from flask_socketio import SocketIO



from flask_mail import Mail
from flask_babel import Babel
from config import Config

db = SQLAlchemy()
mail = Mail()
babel = Babel()
socketio = SocketIO()

root_directory = os.path.abspath(os.path.join(os.getcwd(), 'application'))
root_directory = root_directory + '/'
video_directory = os.path.abspath(os.path.join(root_directory, 'static', 'Videos'))
video_directory = video_directory + '/'

video_streams = dict()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# socketio = SocketIO(app)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

db.init_app(app)
mail.init_app(app)
babel.init_app(app)
socketio.init_app(app)

# from application.Blueprints.HomePage.home_page import home_page
# from application.Blueprints.Dashboard.dashboard import dashboard
# from application.Blueprints.VideoGallery.video_gallery import video_gallery

# app.register_blueprint(home_page)
# app.register_blueprint(dashboard)
# app.register_blueprint(video_gallery)


def create_app():

    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['TWILIO_ACCOUNT_SID'] = 'ACeb42d754baacf9cda420485c10ac5e07'
    app.config['TWILIO_AUTH_TOKEN'] = '490a7f9b7896a3ac79f378cd7e45f768'
    app.config['TWILIO_VERIFY_SERVICE_SID'] = 'VA47f896360d18d82d79bbf6267c72ed1d'
    
    
    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    socketio.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'user_login.show_user_login'
    login_manager.init_app(app)
    
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from application.Blueprints.HomePage.home_page import home_page
    from application.Blueprints.Dashboard.dashboard import dashboard
    from application.Blueprints.VideoGallery.video_gallery import video_gallery
    from application.Blueprints.UserProfile.user_profile import user_profile
    from application.Blueprints.UserLogin.user_login import user_login
    from application.Blueprints.UserSignup.user_signup import user_signup
    from application.Blueprints.UserLogout.user_logout import user_logout
    from application.Blueprints.User2FA.user2fa import user2fa
    from application.Blueprints.UserResetPassword.user_reset_password import user_reset_password
    
    app.register_blueprint(home_page)
    app.register_blueprint(dashboard)
    app.register_blueprint(video_gallery)
    app.register_blueprint(user_profile)
    app.register_blueprint(user_login)
    app.register_blueprint(user_signup)
    app.register_blueprint(user_logout)
    app.register_blueprint(user2fa)
    app.register_blueprint(user_reset_password)

    return app, socketio

