from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from application.VideoStream.VideoFeed import VideoStream

db = SQLAlchemy()
root_directory = os.path.abspath(os.path.join(os.getcwd(), 'application'))
root_directory = root_directory + '/'
print(root_directory)
video_directory = os.path.abspath(os.path.join(root_directory, 'static', 'Videos'))
video_directory = video_directory + '/'
print(video_directory)

print(root_directory)
video_stream = VideoStream()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from application.Blueprints.HomePage.home_page import home_page
    from application.Blueprints.Dashboard.dashboard import dashboard
    from application.Blueprints.VideoGallery.video_gallery import video_gallery
    from application.Bluprints.UserRegistrationAndLogin.user_registration_and_login import user_registration_and_login
    from application.Blueprints.UserRegistrationAndLogin_MainPage.user_registration_and_login_main_page import user_registration_and_login_main_page
    app.register_blueprint(home_page)
    app.register_blueprint(dashboard)
    app.register_blueprint(video_gallery)
    app.register_blueprint(user_registration_and_login)
    app.register_blueprint(user_registration_and_login_main_page)

    return app
