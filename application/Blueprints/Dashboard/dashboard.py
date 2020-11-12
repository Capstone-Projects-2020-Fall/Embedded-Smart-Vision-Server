# home_page.py
# import the necessary packages
from flask import Blueprint, render_template, Response
from ... import video_streams
from ...SocketInterface import SocketInterface

dashboard = Blueprint('dashboard', __name__,
                      template_folder='templates',
                      static_folder='dashboard_static')


@dashboard.route('/dashboard')
def show_nodes():
    sock_interface: SocketInterface = SocketInterface.getInstance()
    nodes = sock_interface.get_node_list()
    print("Showing nodes!", nodes)
    return render_template('dashboard.html', current_page='dashboard', nodes=nodes)


@dashboard.route('/dashboard/liveFeed/<node>')
def show_live_video(node):
    print("Show_Live_Video: ", node)
    return render_template('live_video.html', current_page='dashboard', node=node)


def gen(stream):
    while True:
        frame = stream.get_current_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@dashboard.route('/videoFeed/<node>')
def video_feed(node):
    print("Showing node: ", node)
    if node not in video_streams:
        print("unknown node accessed")
    print("Grabbing Video Stream")
    video_stream = video_streams.get(node)
    print("Got this video Stream", video_stream)
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
