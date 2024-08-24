### Video camera streaming client

#### Project description
Video camera streaming application is a desktop app which is considered to be client side of 
<br> of the following application which is found on [Video camera streaming Server](https://github.com/djaliloua/androidvideostreamServer)
.<br> Once the server is alive, it will get connected to it and then the frames start streaming between both devices.
<br>The desktop application needs the ip address of which shown on server device(android).
<br>NB: Both devices must be connected to the same local network
#### Used libraries
 - Opencv
 - socket
 - Flet
### Flet CLI command to compile to windows exe
 - flet pack main.py --icon icon.ico --name VideoDesktopClient --product-name StreamingVideo --product-version 4.0.0.0

