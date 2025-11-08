This project implements a client–server communication channel using raw TCP sockets in Python.
The client can send Linux OS commands to the server, which executes them and returns the output in JSON format.

Features

1- Lightweight JSON-over-TCP RPC framework.
2- Supports single and batch command execution.
3- Concurrency via ThreadPoolExecutor.
4- Error codes for predictable client handling.
