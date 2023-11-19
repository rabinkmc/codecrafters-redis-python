import socket
from threading import Thread


def handle_request(sock):
    while raw_data := sock.recv(1024):
        print(raw_data.decode())
        data = raw_data.decode().strip("\r\n").split("\r\n")
        print(data)
        if len(data) == 5 and data[2].upper() == "ECHO":
            response = f"+{data[-1]}\r\n"
            sock.send(response.encode())
        else:
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
