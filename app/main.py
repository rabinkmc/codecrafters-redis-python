import socket
from threading import Thread


storage = {}
BUFFER_SIZE = 1024


def handle_request(sock):
    while raw_data := sock.recv(BUFFER_SIZE):
        data = raw_data.decode().strip("\r\n").split("\r\n")
        print(data, len(data))
        if b"ping" in raw_data:
            sock.send(b"+PONG\r\n")
        elif len(data) == 7 and data[2].lower() == "set":
            key = data[4]
            value = data[-1]
            storage[key] = value
            sock.send(b"+OK\r\n")
        elif len(data) == 5 and data[2].lower() == "get":
            key = data[-1]
            value = storage[key]
            response = f"${len(value)}\r\n{value}\r\n"
            sock.send(response.encode())
        elif len(data) == 5 and data[2].lower() == "echo":
            response = f"+{data[-1]}\r\n"
            sock.send(response.encode())
        else:
            sock.send(b"-Error: unknown command \r\n")
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
