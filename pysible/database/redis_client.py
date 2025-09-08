import os
from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_HOST = os.getenv("redis_host")
REDIS_PORT = os.getenv("redis_port")
REDIS_DB_TO_USE = os.getenv("redis_db_no")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_TO_USE)

