import socket
from threading import Thread
import time


def handle_request(sock):
    while sock.recv(1024):
        sock.send(b"+PONG\r\n")
    sock.close()


def main():
    print("Initializing redis server:")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        sock, _ = server_socket.accept()
        thread = Thread(target=handle_request, args=(sock,))
        thread.start()


if __name__ == "__main__":
    main()
