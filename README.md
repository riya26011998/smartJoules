## Remote Command Executor

This project implements a **client–server communication system** using **raw TCP sockets** in Python.  
The client sends Linux OS commands to the server, which executes them and sends JSON responses.

---

## Features
- Execute any Linux OS command remotely  
- Supports **single and batch** requests  
- Concurrency using **ThreadPoolExecutor**  
- JSON response with error codes  

---

## Usage

### Start the Server
```bash
python3 server.py
