# RQ Worker Entrypoint 
# [[to runs the RQ worker process which listens to the Redis queue, picks up jobs on Background]]

import redis
from redis import Redis
from rq import SimpleWorker, Queue

# The queues the worker will listen to.
listen = ['default']

# Redis connection details.
redis_url = 'redis://localhost:6379'
conn: Redis = redis.from_url(redis_url)

if __name__ == '__main__':
    # Create a list of Queue objects to listen to.
    queues = [Queue(name, connection=conn) for name in listen]
    
    # Create a new worker that listens on the specified queues.
    # SimpleWorker runs jobs in the same process (no fork) — Windows friendly.
    worker = SimpleWorker(queues, connection=conn)
    print("Starting SimpleWorker (Windows-compatible). Press Ctrl+C to stop")
    worker.work()