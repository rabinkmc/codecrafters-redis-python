import socket
from threading import Thread

storage = {}


def handle_request(sock):
    while raw_data := sock.recv(1024):
        print(raw_data.decode())
        data = raw_data.decode().strip("\r\n").split("\r\n")
        print(data)
        if len(data) == 7 and data[2].lower() == "set":
            key = data[4]
            value = data[-1]
            storage[key] = value
            sock.send(b"+OK\r\n")
        if len(data) == 5 and data[2].lower() == "get":
            key = data[-1]
            sock.send(f"+{storage[key]}\r\n".encode())
        if len(data) == 5 and data[2].lower() == "echo":
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
