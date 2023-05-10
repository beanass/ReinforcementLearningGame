import socket
import json

HOST = '127.0.0.1'
PORT = 8080
# Define the file name
file_name = 'game_state.json'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    with open(file_name, 'w', encoding='utf-8') as f:
        while True:
            data = s.recv(8192)
            print(f"Received {data!r}")
            print(type(data))
            json.dump(data.decode(), f, ensure_ascii=False, indent=4)