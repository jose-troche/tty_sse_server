from __future__ import print_function

import signal
import pyuv
import sys

# This is a pyuv (event loop) implementation of a server that listens
# with no blocking to tty stdin (e.g. a serial port) and sends the read data
# to browsers that connect via TCP using Server Side Events (EventSource)
#
# Usage example:
#     python tty_sse_server.py < /dev/tty.Bluetooth-Serial
# 
# Will listen to tty.Bluetooth-Serial and send input to browsers that connected
# via EventSource
#
#
# On the client side the only code needed is EventSource. You can try this in 
# the browser console:
#
# var eventSource = new EventSource('http://localhost:1234/')
# eventSource.addEventListener('message', function(e){console.log(e.data);}, false);
#
# That will start printing the serial port input data
# To close the connection:
# 
# eventSource.close()
# 
# Dependencies: pyuv. Install with:
# sudo pip install pyuv


def on_connection(server, error):
    client = pyuv.TCP(server.loop)
    server.accept(client)
    clients.append(client)
    client.start_read(on_read)
    client.write(get_response('Init'))
    print("+++ TCP client accepted. # of clients %d" % len(clients))

def send_response_to_clients(data=None):
    for client in clients:
        client.write(get_response(data))

# Access-Control-Allow-Origin is needed for Cross Origin Resource Sharing (CORS)
# so that calls from a different domains can be made. Replace * by a specific
# server
HEADERS = """
HTTP/1.1 200 OK
Cache-Control: no-cache
Access-Control-Allow-Origin: *
Content-Type: text/event-stream

"""

def get_response(data=None):
    return (HEADERS +
        'data: %s\n\n' % data
    )

def on_read(client, data, error):
    if data is None:
        client.close()
        clients.remove(client)
        print("--- TCP client dropped. # of clients %d" % len(clients))
        return

def on_tty_read(handle, data, error):
    if data is None or data == b"exit":
        shutdown()
    else:
        send_response_to_clients(data)

def signal_cb(handle, signum):
    shutdown()

def shutdown():
    [c.close() for c in clients]
    if not tty_stdin.closed:
        tty_stdin.close()
    server.close()
    signal_h.close()
    

loop = pyuv.Loop.default_loop()

# The list of TCP clients connected to server
clients = []

# TCP listener bound to any IP assigned to this machine and por 1234
server = pyuv.TCP(loop)
server.bind(("0.0.0.0", 1234))
server.listen(on_connection)

# TTY standard input listener
tty_stdin = pyuv.TTY(loop, sys.stdin.fileno(), True)
tty_stdin.start_read(on_tty_read)

# KILL signal handler
signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

(ip, port) = server.getsockname()
print ("Serving on %s:%s " % (ip, port) )

loop.run()

pyuv.TTY.reset_mode()
print("Stopped!")
