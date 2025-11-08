import threading
import time
import uuid
from client import Client
from server import Server
import pytest

# Start server in a background thread

def start_server_in_thread():
    s = Server()
    thread = threading.Thread(target=s.start, daemon=True)
    thread.start()
    time.sleep(1)  # wait for server to start
    return thread

@pytest.fixture(scope="module")
def running_server():
    t = start_server_in_thread()
    yield
    # stops with main process

# Integration tests: Client to Server

def test_client_server_integration(running_server):
    client = Client()
    client.connect("127.0.0.1", 9999)

    req = {"method": "echo integration_test", "id": str(uuid.uuid4())}
    resp = client.request(req)

    assert resp["result"] == 0
    assert "integration_test" in resp["stdout"]

    client.close()

def test_client_server_batch(running_server):
    client = Client()
    client.connect("127.0.0.1", 9999)

    batch = [
        {"method": "echo batch1", "id": "1"},
        {"method": "echo batch2", "id": "2"},
        {"method": "echo batch3", "id": "3"}
    ]

    resp = client.request(batch)
    assert isinstance(resp, list)
    assert len(resp) == 3
    ids = {r["id"] for r in resp}
    assert ids == {"1", "2", "3"}

    client.close()
