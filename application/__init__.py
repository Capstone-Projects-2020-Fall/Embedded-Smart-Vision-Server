from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from application.VideoStream.VideoFeed import VideoStream
from flask_socketio import SocketIO

db = SQLAlchemy()

root_directory = os.path.abspath(os.path.join(os.getcwd(), 'application'))
root_directory = root_directory + '/'
video_directory = os.path.abspath(os.path.join(root_directory, 'static', 'Videos'))
video_directory = video_directory + '/'

video_streams = dict()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
socketio = SocketIO(app)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

db.init_app(app)

from application.Blueprints.HomePage.home_page import home_page
from application.Blueprints.Dashboard.dashboard import dashboard
from application.Blueprints.VideoGallery.video_gallery import video_gallery

app.register_blueprint(home_page)
app.register_blueprint(dashboard)
app.register_blueprint(video_gallery)


def create_app():
    return app, socketio
