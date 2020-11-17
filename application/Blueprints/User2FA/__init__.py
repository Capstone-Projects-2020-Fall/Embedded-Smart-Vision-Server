from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from application.VideoStream.VideoFeed import VideoStream
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()

root_directory = os.path.abspath(os.path.join(os.getcwd(), 'application'))
root_directory = root_directory + '/'
video_directory = os.path.abspath(os.path.join(root_directory, 'static', 'Videos'))
video_directory = video_directory + '/'

video_streams = dict()


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)
    bootstrap.init_app(app)
    
    login_manager = LoginManager()
    login_manger.login_view = 'user_login.show_user_login'
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
    
    app.register_blueprint(home_page)
    app.register_blueprint(dashboard)
    app.register_blueprint(video_gallery)
    app.register_blueprint(user_profile)
    app.register_blueprint(user_login)
    app.register_blueprint(user_signup)
    app.register_blueprint(user_logout)

    return app
