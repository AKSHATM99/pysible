from pysible.database.db import redis_client

keys = redis_client.hget("user_id:DFU1", "roles").decode().split(",")
# user_ids = [key.decode().split("user_id:", "roles")[1] for key in keys]
print(keys)