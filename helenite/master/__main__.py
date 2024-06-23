import asyncio
import logging
import uuid

import grpc
from google.protobuf.wrappers_pb2 import BoolValue
from redis import Redis

from helenite.core.core_pb2 import (
    AllocateChunkRequest,
    ChunkHandle,
    ChunkInformation,
    ChunkServerInformation,
    CreateFileRequest,
)
from helenite.master import config, master_pb2_grpc


class MasterServicer(master_pb2_grpc.MasterServicer):
    def __init__(self) -> None:
        self.redis = Redis.from_url(config.REDIS_URL, decode_responses=True)

    async def CreateFile(self, request: CreateFileRequest, context) -> BoolValue:
        return BoolValue(value=True)

    def AllocateChunk(self, request: AllocateChunkRequest, context):
        handle = ChunkHandle(handle=uuid.uuid4().hex)

    def GetChunkInformation(self, request: ChunkHandle, context) -> ChunkInformation:
        return super().GetChunkInformation(request, context)

    async def RegisterChunkServer(
        self, request: ChunkServerInformation, context
    ) -> BoolValue:
        try:
            await self.redis.sadd("chunk_servers", f"{request.address}:{request.port}")
            logging.info(
                f"Registered chunk server {request.address}:{request.port} successfully"
            )
            return BoolValue(value=True)
        except Exception:
            logging.exception(
                f"Failed to register chunk server {request.address}:{request.port}"
            )
            return BoolValue(value=False)


async def serve() -> None:
    server = grpc.aio.server()
    master_pb2_grpc.add_MasterServicer_to_server(MasterServicer(), server)
    server.add_insecure_port("[::]:50051")
    logging.info("Starting server on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    asyncio.run(serve())
