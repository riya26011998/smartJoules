import pytest
import socket
from client import Client
import json
import uuid

# Unit tests for Client class

def test_client_initialization():
    """Client object should initialize correctly."""
    c = Client()
    assert c.sock is None

def test_client_connect_close(monkeypatch):
    """Test connecting and closing the client socket."""
    c = Client()
    fake_sock = type('FakeSocket', (), {'connect': lambda self, addr: None, 'close': lambda self: None})()
    monkeypatch.setattr(c, 'sock', fake_sock)
    c.close()  # Should not raise exception

def test_client_request_single(monkeypatch):
    """Test sending a single request."""
    c = Client()

    # Fake socket to simulate server response
    class FakeSocket:
        def sendall(self, data):
            self.sent_data = data
        def recv(self, bufsize):
            # Echo back the JSON request as response
            return b'{"result":0,"stdout":"hello\\n","stderr":"","id":"123","error_code":0}'
        def close(self):
            pass

    c.sock = FakeSocket()

    req = {"method": "echo hello", "id": "123"}
    resp = c.request(req)

    assert isinstance(resp, dict)
    assert resp["stdout"] == "hello\n"
    assert resp["id"] == "123"

def test_client_request_batch(monkeypatch):
    """Test sending a batch of requests."""
    c = Client()

    class FakeSocket:
        def sendall(self, data):
            self.sent_data = data
        def recv(self, bufsize):
            # Return a list of response objects
            return json.dumps([
                {"result": 0, "stdout": "1\n", "stderr": "", "id": "1", "error_code": 0},
                {"result": 0, "stdout": "2\n", "stderr": "", "id": "2", "error_code": 0}
            ]).encode()
        def close(self):
            pass

    c.sock = FakeSocket()

    batch_req = [
        {"method": "echo 1", "id": "1"},
        {"method": "echo 2", "id": "2"}
    ]

    resp = c.request(batch_req)
    assert isinstance(resp, list)
    assert len(resp) == 2
    assert resp[0]["id"] == "1"
    assert resp[1]["id"] == "2"

