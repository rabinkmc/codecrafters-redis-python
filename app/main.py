import socket
from threading import Thread
from datetime import datetime, timedelta
import argparse
from app.rdb_parser import RDBParser
from pathlib import Path


database = {}
BUFFER_SIZE = 1024


def handle_get(sock, key, rdb=None):
    redis_data = database
    if rdb:
        redis_data = rdb.key_values
    if key not in redis_data:
        response = "$-1\r\n"
        sock.send(response.encode())
        return
    value, ttl = redis_data[key]
    value = str(value)
    if ttl and ttl < datetime.now():
        del redis_data[key]
        response = "$-1\r\n"
        sock.send(response.encode())
    else:
        response = f"${len(value)}\r\n{value}\r\n"
        sock.send(response.encode())


def handle_request(sock):
    while raw_data := sock.recv(BUFFER_SIZE):
        data = raw_data.decode().strip("\r\n").split("\r\n")
        if b"ping" in raw_data:
            sock.send(b"+PONG\r\n")
        elif len(data) == 5 and data[2].lower() == "keys" and data[4] == "*":
            path = Path(database["dir"]) / database["dbfilename"]
            rdb_parser = RDBParser(path)
            keys = list(rdb_parser.key_values.keys())
            sock.send(get_arr(*keys).encode())

        elif len(data) >= 7 and data[2].lower() == "set":
            key = data[4]
            value = data[6]
            px = None
            if "px" in data and len(data) >= 11:
                px = data[10]
            ttl = px and (datetime.now() + timedelta(milliseconds=int(px)))
            database[key] = (value, ttl)
            sock.send(b"+OK\r\n")
        elif len(data) == 5 and data[2].lower() == "get":
            key = data[-1]
            if "dir" in database and "dbfilename" in database:
                path = Path(database["dir"]) / database["dbfilename"]
                rdb_parser = RDBParser(path)
                handle_get(sock, key, rdb_parser)
            else:
                handle_get(sock, key)
        elif "config" in data and "get" in data:
            key = data[-1]
            sock.send(get_arr(key, database[key]).encode())

        elif len(data) == 5 and data[2].lower() == "echo":
            response = f"+{data[-1]}\r\n"
            sock.send(response.encode())
        else:
            sock.send(b"-Error: unknown command \r\n")
    sock.close()


def main():
    print("Initializing redis server:")
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="The directory for redis files")
    parser.add_argument("--dbfilename", help="The name of the file database")
    args = parser.parse_args()
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    if args.dir:
        database["dir"] = args.dir
    if args.dbfilename:
        database["dbfilename"] = args.dbfilename

    while True:
        sock, _ = server_socket.accept()
        thread = Thread(target=handle_request, args=(sock,))
        thread.start()


def get_arr_string(str):
    return f"${len(str)}\r\n{str}\r\n"


def get_arr(*args):
    arr = f"*{len(args)}\r\n"
    for arg in args:
        arr = arr + get_arr_string(arg)
    return arr


if __name__ == "__main__":
    main()
