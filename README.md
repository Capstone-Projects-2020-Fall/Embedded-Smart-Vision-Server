# Embedded-Smart-Vision-Server
The server does not need to be built by the testing team. Instead, it should be accessed at the following address http://0.0.0.0:5000/

## Features
* Website can be reached at the above address at all times
* User should be able to navigate among the pages (home page, dashboard, video gallery)
* Node can connect to the central server
* Connected nodes are displayed on the dashboard. Live feed from each node can be viewed at all times
* Connected nodes can upload recorded videos with tags of people found in the video, which can be viewed on the video gallery page

## Known bugs
* Sizing of web page elements is fixed, and some elements may appear to be in the wrong spot depending on the device that accesses the web page 
(in particular the web page will not look good on a phone)
* Videos cannot be opened by the central server. While videos are uploaded along with their tags, the central server cannot open the video and play it. Currently, the video
gallery will only show tags with no accompanying video thumbnail
* If live feed is not working, no frame will be displayed (instead of an image alerting the user live feed cannot be accessed)
* Nodes are still displayed on the dashboard even after they've disconnected. To test if a node is still connected, you (for now) need to click on the node and view the live feed

## Building
To run the server you must have python3 installed on your machine as well as pip (python's tool for downloading dependencies). Download the repository as a zip file and unzip the
file. Using pip, download all of the required dependencies from the attached 'requirements.txt' file using the following command: pip install -r requirements.txt. Then, open the
python3 terminal with the following command: python3. Use the terminal to initialize the database using the following python lines:
1. from application import db, create_app
2. socket_io, app = create_app()
3. app.app_context().push()
4. db.create_all()

If all dependencies are downloaded correctly and database is initialized, the server should start with the following command: python3 StartServer.py
