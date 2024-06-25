import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

REDIS_URL = os.getenv("REDIS_URL_MASTER")
REPLICATION_FACTOR = int(os.getenv("REPLICATION_FACTOR", 1))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1024))
