# This thread will hook up to a specific video feed and process and update the frames as they come in
import threading
import time
from datetime import datetime

from multiprocessing.connection import PipeConnection

import cv2

from application.VideoStream.VideoFeed import VideoStream
from application import socketio


class VideoThread(threading.Thread):

    def __init__(self,
                 name="Not-Set",
                 lf_pipe=None,
                 v_feed=None):
        threading.Thread.__init__(self)
        self.name = name
        self.lf_pipe: PipeConnection = lf_pipe
        self.v_feed: VideoStream = v_feed
        self.running = False
        self.emitter = False
        self.pulse = datetime.now()

    def pulse_emitter(self):
        self.emitter = True
        self.pulse = datetime.now()
        # print("Pulsing emitter: ", self.emitter, self.pulse)

    def run(self):
        print("Starting" + self.name + " Which is a video thread")
        self.running = True
        while self.running:
            # This thread loops around receiving data from the socket server and pushing it to the video stream
            frame = self.lf_pipe.recv()
            # ret, frame_encode = cv2.imencode('.jpg', frame)
            # frame_bytes = frame_encode.tobytes()
            # self.v_feed.update_frame(frame_encode)
            # cv2.imshow('Frame', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            now = datetime.now()
            time_delta = now - self.pulse
            # Check if it has been more then a second since the last pulse
            if time_delta.seconds > 2:
                self.emitter = False
            if self.emitter:
                socketio.emit('frame-'+self.name, bytes(frame))
