class NodeInformation:
    def __init__(self,
                 node_name="not set",
                 stream_connection=None,
                 video_camera=None):
        self.node_name = node_name
        self.stream_connection = stream_connection
        self.video_camera = video_camera
        self.video_thread = None

    def to_string(self):
        return "{0}{1}{2}{3}".format(self.node_name,
                                     str(self.stream_connection),
                                     str(self.video_camera),
                                     str(self.video_thread))
