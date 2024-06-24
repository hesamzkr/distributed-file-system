import logging

import grpc
from google.protobuf.wrappers_pb2 import StringValue
from redis import Redis

from helenite.client import config
from helenite.core import core_pb2_grpc
from helenite.core.core_pb2 import (
    AllocateChunkRequest,
    ChunkHandle,
    CreateFileRequest,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HeleniteClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.master_stub = core_pb2_grpc.MasterStub(self.channel)
        self.redis = Redis.from_url(config.REDIS_URL, decode_responses=True)

    async def create_file(self, filename, size):
        request = CreateFileRequest(filename=filename, size=size)
        response = self.master_stub.CreateFile(request)
        await self.redis.hmset(f"file:{request.filename}", mapping={"size": request.size})
        logger.info(f"CreateFile response: {response.value}")
        return response.value

    def delete_file(self, filename):
        request = StringValue(value=filename)
        response = self.master_stub.DeleteFile(request)
        self.redis.delete(f"file:{filename}")
        logger.info(f"DeleteFile response: {response.value}")
        return response.value

    async def allocate_chunk(self, filename, sequence_number):
        request = AllocateChunkRequest(filename=filename, sequence_number=sequence_number)
        response = self.master_stub.AllocateChunk(request)
        chunk_info = {
            "handle": response.handle.handle,
            "sequence_number": sequence_number,
            "servers": ",".join([server.address for server in response.servers])
        }
        await self.redis.hmset(f"file:{filename}:chunk:{sequence_number}", mapping=chunk_info)
        logger.info(f"AllocateChunk response: {response}")
        return response

    def get_chunk_information(self, handle):
        request = ChunkHandle(handle=handle)
        response = self.master_stub.GetChunkInformation(request)
        logger.info(f"GetChunkInformation response: {response}")
        return response