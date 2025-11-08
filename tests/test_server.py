from server import Server

def test_server_initialization():
    s = Server(host="0.0.0.0", port=9999)
    assert s.host == "0.0.0.0"
    assert s.port == 9999
