import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MASTER_ADDRESS = os.getenv("MASTER_ADDRESS", "localhost:50051")
REDIS_URL = os.getenv("REDIS_URL")
