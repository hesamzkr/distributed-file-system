import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1024))
MASTER_ADDRESS = os.getenv("MASTER_ADDRESS", "localhost:50051")
HOST = os.getenv("HOST", "localhost")
CHUNKS_DIR = os.getenv("CHUNKS_DIR", "chunks")
NAMESPACE_DIR = os.getenv("NAMESPACE_DIR", "namespace")
