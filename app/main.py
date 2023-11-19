import socket


def main():
    print("Initializing redis server:")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    sock, _ = server_socket.accept()
    sock.recv(1024)
    sock.send(b"+PONG\r\n")
    sock.close()


if __name__ == "__main__":
    main()
