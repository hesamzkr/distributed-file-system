import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

REDIS_URL = os.getenv("REDIS_URL")
