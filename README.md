# Embedded-Smart-Vision-Server
The server does not need to be built by the testing team. Instead, it should be accessed at the following address http://45.79.152.222:5000/

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
