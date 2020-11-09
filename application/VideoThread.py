# This thread will hook up to a specific video feed and process and update the frames as they come in
import threading

from multiprocessing.connection import PipeConnection

import cv2

from application.VideoStream.VideoFeed import VideoStream


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

    def run(self):
        print("Starting" + self.name + " Which is a video thread")
        self.running = True
        while self.running:
            frame = self.lf_pipe.recv()
            self.v_feed.update_frame(frame)
