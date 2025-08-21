# RQ Worker Entrypoint 
# [[to runs the RQ worker process which listens to the Redis queue, picks up jobs on Background]]
import redis
from redis import Redis
from rq import Connection, Worker, Queue # type: ignore [[ ignore library's type hints ]]

# [[ Queue the worker will listen to. 'default' is the standard one. ]]
listen = ['default']

# Redis connection details.
redis_url = 'redis://localhost:6379'
conn: Redis = redis.from_url(redis_url) # type: ignore [[ ignore type hints warning for library ]]

if __name__ == '__main__':
    with Connection(conn):
        # Create a new worker that listens on the specified queues
        worker = Worker(map(Queue, listen))
        print(f"Worker starting... Listening on queue: {', '.join(listen)}")
        worker.work()