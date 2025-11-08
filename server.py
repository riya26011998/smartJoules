import socket
import json
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor

MAX_WORKERS = 10
BUFFER_SIZE = 4096

class Server:
    def __init__(self, host="0.0.0.0", port=9999):
        self.host = host
        self.port = port

    def start(self):
        """Start the server and listen for client connections."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(5)
            print(f"[+] Server listening on {self.host}:{self.port}")

            while True:
                client_sock, addr = s.accept()
                print(f"[+] Connection from {addr}")
                threading.Thread(target=self.handle_client, args=(client_sock,)).start()

    def handle_client(self, client_sock):
        """Handle each client connection."""
        with client_sock:
            data = client_sock.recv(BUFFER_SIZE)
            if not data:
                return

            try:
                payload = json.loads(data.decode())
            except json.JSONDecodeError:
                response = {"error_code": 1, "error": "JSON parse error"}
                client_sock.sendall((json.dumps(response) + "\n").encode())
                return

            if isinstance(payload, list):
                responses = self.handle_batch(payload)
            else:
                responses = self.process_request(payload)

            response_data = json.dumps(responses)
            client_sock.sendall((response_data + "\n").encode())

    def handle_batch(self, requests):
        """Handle multiple requests concurrently."""
        results = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(self.process_request, req) for req in requests]
            for f in futures:
                results.append(f.result())
        return results

    def process_request(self, req):
        """Execute OS command from the request."""
        try:
            cmd = req.get("method")
            req_id = req.get("id")

            if not cmd or not req_id:
                return {
                    "result": None,
                    "stdout": "",
                    "stderr": "Invalid request format",
                    "id": req.get("id"),
                    "error_code": 2,
                }

            try:
                proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return {
                    "result": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "id": req_id,
                    "error_code": 0 if proc.returncode == 0 else 3,
                }
            except Exception as e:
                return {
                    "result": None,
                    "stdout": "",
                    "stderr": str(e),
                    "id": req_id,
                    "error_code": 4,
                }

        except Exception as e:
            return {
                "result": None,
                "stdout": "",
                "stderr": str(e),
                "id": req.get("id", "unknown"),
                "error_code": 4,
            }
