import redis
from rq import Queue

# Configure Redis connection.
redis_conn = redis.Redis() # [[ For local development ]]

# Variable for handle queue.
q = Queue(connection=redis_conn)