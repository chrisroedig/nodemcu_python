import time
import json
import socket

class HttpPoller():
    def __init__(self, url, method = 'GET', on_data=None, poll_delay=1500, response_delay=500):
        self.running = False
        self.method = method
        self.headers = {}
        self.json = None
        self.data = None
        self.response_headers = {}
        self.response_data = None
        self.response_json = None
        self.data_callback = on_data
        self.state = 0
        self.poll_delay = poll_delay
        self.response_delay = response_delay
        self.sequence = [
            self.connect_socket,
            self.send_request,
            self.start_response_wait,
            self.wait,
            self.receive_response,
            self.start_poll_wait,
            self.wait
        ]
        self.wait_stop_time = None
        if time.__name__ == 'utime':
            self.time = time.ticks_ms
        else:
            self.time = lambda :time.time() * 1000
        self.setup(url)
    def setup(self, url):
        try:
            self.proto, dummy, self.host, self.path = url.split("/", 3)
        except ValueError:
            self.proto, dummy, self.host = url.split("/", 2)
            self.path = ""
        if self.proto == "http:":
            self.port = 80
        else:
            raise ValueError("SSL not yet implemented")
        if ":" in self.host:
            self.host, self.port = self.host.split(":", 1)
            self.port = int(self.port)
        if not "Host" in self.headers:
            self.headers['Host'] = self.host

    def operate(self):
        seq_fn = self.sequence[self.state]
        if seq_fn():
            self.state +=1
        if self.state >= len(self.sequence):
            self.state = 0

    def connect_socket(self):
        ai = socket.getaddrinfo(self.host, self.port,  0, socket.SOCK_STREAM)[0]
        self.sock = socket.socket(ai[0], ai[1], ai[2])
        self.sock.connect(ai[-1])
        return True

    def send_request(self):
        self.socket_send('%s /%s HTTP/1.0\r\n' % (self.method, self.path))
        for k in self.headers:
            self.socket_send(k+": "+self.headers[k]+"\r\n")
        if self.json is not None:
            assert self.data is None
            self.data = json.dumps(self.json)
            self.socket_send("Content-Type: application/json\r\n")
        if self.data:
            self.socket_send("Content-Length: %d\r\n" % len(data))
        self.socket_send("\r\n")
        if self.data:
            self.sock.send(data)
        return True

    def start_response_wait(self):
        self.wait_stop_time = self.time() + self.response_delay
        return True

    def wait(self):
        if self.wait_stop_time == None:
            return True
        if self.wait_stop_time < self.time():
            return True
        return False

    def receive_response(self):
        self.sock = self.sock.makefile()
        resp = str(self.sock.readline(), 'utf8')
        self.proto, self.status, self.reason = resp.split(' ',2)
        self.read_headers()
        if self.response_headers.get('Transfer-Encoding') == 'chunked':
            self.read_content_chunked()
        else:
            self.read_content()
        self.sock.close()
        self.parse_content()
        if self.data_callback is not None:
            if self.response_json is not None:
                self.data_callback(self.response_json)
            else:
                self.data_callback(self.response_data)
        return True

    def start_poll_wait(self):
        self.wait_stop_time = self.time() + self.poll_delay
        return True

    def socket_send(self, data_str):
        self.sock.send(bytes(data_str,'utf8'))

    def read_headers(self):
        self.response_headers = {}
        while True:
            line = self.sock.readline()
            if not line or line == b'\r\n':
                break
            header_pair = str(line, 'utf-8').split(': ')
            if len(header_pair) < 2:
                break
            self.response_headers[header_pair[0]] = header_pair[1][:-2]

    def read_content_chunked(self):
        self.response_data = ''
        while True:
            size_str = str(self.sock.readline(), 'utf8')
            size = int('0x%s' % size_str[:-2],16)
            if size == 0:
                break
            self.response_data += str(self.sock.readline(), 'utf8')

    def read_content(self):
        self.response_data = self.sock.read()

    def parse_content(self):
        if self.response_headers.get('Content-Type') == 'application/json':
            self.response_json = json.loads(self.response_data)

## Example
# if __name__ == '__main__':
#
#     # in the setup pahse of your program
#     poller=HttpPoller('<url here>', on_data = on_new_data)
#     def on_new_data(data):
#           print(data)
#
#     # your program's main loop
#     while True:
#         poller.operate() # tell the poller to do something
#         # do other stuff
