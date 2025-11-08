import pytest
import json
from client import Client

# Fake socket to simulate server

class FakeSocket:
    def __init__(self, response):
        self.response = response.encode()
        self.sent_data = None
    def sendall(self, data):
        self.sent_data = data
    def recv(self, bufsize):
        return self.response
    def close(self):
        pass

# Unit tests for Client

def test_client_initialization():
    c = Client()
    assert c.sock is None

def test_client_request_single():
    c = Client()
    c.sock = FakeSocket('{"result":0,"stdout":"hello\\n","stderr":"","id":"123","error_code":0}')
    req = {"method": "echo hello", "id": "123"}
    resp = c.request(req)
    assert resp["stdout"] == "hello\n"
    assert resp["id"] == "123"

def test_client_request_batch():
    c = Client()
    batch_response = json.dumps([
        {"result":0,"stdout":"1\n","stderr":"","id":"1","error_code":0},
        {"result":0,"stdout":"2\n","stderr":"","id":"2","error_code":0}
    ])
    c.sock = FakeSocket(batch_response)
    batch_req = [
        {"method": "echo 1", "id": "1"},
        {"method": "echo 2", "id": "2"}
    ]
    resp = c.request(batch_req)
    assert isinstance(resp, list)
    assert len(resp) == 2
    assert {r["id"] for r in resp} == {"1","2"}
