import pytest
from server import Server

# Unit tests for Server

def test_server_initialization():
    s = Server(host="0.0.0.0", port=9999)
    assert s.host == "0.0.0.0"
    assert s.port == 9999

def test_process_valid_command():
    s = Server()
    req = {"method": "echo hello", "id": "123"}
    res = s.process_request(req)
    assert res["result"] == 0
    assert "hello" in res["stdout"]
    assert res["error_code"] == 0

def test_process_invalid_command():
    s = Server()
    req = {"method": "invalidcommand123", "id": "456"}
    res = s.process_request(req)
    assert res["result"] != 0
    assert res["error_code"] == 3

def test_process_missing_fields():
    s = Server()
    req = {"method": "echo hello"}  # missing id
    res = s.process_request(req)
    assert res["error_code"] == 2
