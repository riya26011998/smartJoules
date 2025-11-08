import subprocess
import time
from client import Client
from server import Server
import threading
import uuid

def start_server():
    s = Server()
    threading.Thread(target=s.start, daemon=True).start()
    time.sleep(1)

def test_client_server_integration():
    start_server()
    client = Client()
    client.connect("127.0.0.1", 9999)

    req = {"method": "echo hello", "id": str(uuid.uuid4())}
    resp = client.request(req)
    assert "stdout" in resp
    client.close()
