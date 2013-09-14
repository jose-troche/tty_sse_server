tty_sse_server
==============

HTTP **Server Side Events** server based on pyuv that listens to stdin as TTY (e.g serial port) and pushes its data to browser via SSE


This is a pyuv (event loop) implementation of a server that listens
with no blocking to tty stdin (e.g. a serial port) and sends the read data
to browsers that connect via TCP using Server Side Events (EventSource)

Usage example:
```
    python tty_sse_server.py < /dev/tty.Bluetooth-Serial
```

Will listen to tty.Bluetooth-Serial and send input to browsers connected
via EventSource


On the client side the only code needed is EventSource. You can try this in 
the browser console:

```
var eventSource = new EventSource('http://localhost:1234/')
eventSource.addEventListener('message', function(e){console.log(e.data);}, false);
```

That will start printing the serial port input data
To close the connection:

```
eventSource.close()
```

Dependencies: pyuv. Install with:
```
sudo pip install pyuv
```
