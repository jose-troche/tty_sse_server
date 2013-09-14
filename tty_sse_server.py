from __future__ import print_function

import signal
import pyuv
import sys

def on_connection(server, error):
    client = pyuv.TCP(server.loop)
    server.accept(client)
    clients.append(client)
    client.start_read(on_read)
    client.write(get_response('Init'))
    print("+++ TCP client accepted. # of clients %d" % len(clients))

def on_timeout(timer_handle):
    pass
    #send_response_to_clients()

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
    timer.close()
    signal_h.close()
    

loop = pyuv.Loop.default_loop()
clients = []

server = pyuv.TCP(loop)
server.bind(("0.0.0.0", 1234))
server.listen(on_connection)

signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

tty_stdin = pyuv.TTY(loop, sys.stdin.fileno(), True)
tty_stdin.start_read(on_tty_read)

timer =  pyuv.Timer(loop)
REPEAT_RATE = 1.0  # Float Secs
timer.start(on_timeout, 0, REPEAT_RATE)

(ip, port) = server.getsockname()
print ("Serving on %s:%s " % (ip, port) )

loop.run()

pyuv.TTY.reset_mode()
print("Stopped!")
