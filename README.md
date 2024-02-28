[![progress-banner](https://backend.codecrafters.io/progress/redis/da197006-7d99-4ec4-95a6-03c2808e15bf)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a starting point for Python solutions to the
["Build Your Own Redis" Challenge](https://codecrafters.io/challenges/redis).

In this challenge, you'll build a toy Redis clone that's capable of handling
basic commands like `PING`, `SET` and `GET`. Along the way we'll learn about
event loops, the Redis protocol and more.

We'll learn to parse RDB files from the following specifications.[RDB Spec](https://rdb.fnordig.de/file_format.html)

The entry point for Redis implementation is in `app/main.py`. 

1. Ensure you have `python (3.x)` installed locally
1. Run `./spawn_redis_server.sh` to run your Redis server, which is implemented
   in `app/main.py`.
