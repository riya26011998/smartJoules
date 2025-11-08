import socket
import json

BUFFER_SIZE = 4096

class Client:
    def __init__(self):
        self.sock = None

    def connect(self, host_ip="127.0.0.1", port=9999):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host_ip, port))

    def request(self, req_obj):
        """Send a single or batch request and receive the response."""
        data = json.dumps(req_obj).encode()
        self.sock.sendall(data)

        response_data = self.sock.recv(BUFFER_SIZE)
        response = json.loads(response_data.decode())
        return response

    def close(self):
        if self.sock:
            self.sock.close()
