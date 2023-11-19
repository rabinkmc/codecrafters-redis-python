import socket


def handle_request(sock):
    while sock.recv(1024):
        sock.send(b"+PONG\r\n")
    sock.close()


def main():
    print("Initializing redis server:")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    sock, _ = server_socket.accept()
    handle_request(sock)


if __name__ == "__main__":
    main()
