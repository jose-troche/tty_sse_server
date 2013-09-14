from __future__ import print_function

import signal
import pyuv

import time

def on_connection(server, error):
    client = pyuv.TCP(server.loop)
    server.accept(client)
    clients.append(client)
    client.start_read(on_read)
    print("+++ Client accepted. # of clients %d" % len(clients))

def on_timeout(timer_handle):
    for client in clients:
        client.write(get_response())

HEADERS = """
HTTP/1.1 200 OK
Cache-Control: no-cache
Content-Type: text/event-stream

"""

def get_response():
    return (HEADERS +
        'data: %s\n\n' % str(time.time())
    )

def on_read(client, data, error):
    if data is None:
        client.close()
        clients.remove(client)
        print("--- Client dropped. # of clients %d" % len(clients))
        return

def signal_cb(handle, signum):
    [c.close() for c in clients]
    signal_h.close()
    server.close()
    timer.close()

loop = pyuv.Loop.default_loop()
clients = []

server = pyuv.TCP(loop)
server.bind(("0.0.0.0", 1234))
server.listen(on_connection)

signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

timer =  pyuv.Timer(loop)
REPEAT_RATE = 1.0  # Float Secs
timer.start(on_timeout, 0, REPEAT_RATE)

(ip, port) = server.getsockname()
print ("Serving on %s:%s " % (ip, port) )

loop.run()
print("Stopped!")
