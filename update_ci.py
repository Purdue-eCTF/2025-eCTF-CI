import os
import socket
import sys

if __name__ == "__main__":
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((os.environ["IP"], int(os.environ["PORT"])))
    conn.send(f"{os.environ['TOKEN']}|update-ci".encode())
    ack = conn.recv(1024).decode()

    if not ack or "Invalid" in ack:
        print("Connection error")
        sys.exit(1)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        line = data.decode(errors="ignore")
        if "%*&" in line:
            print(line[: (line.find("%*&"))])
            sys.exit(int(line[(line.find("%*&") + 3) :].split("\n")[0]))
        print(line, end="")
