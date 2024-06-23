import asyncio
import logging

import grpc

from helenite.core.core_pb2 import (
    AllocateChunkRequest,
    ChunkHandle,
    ChunkInformation,
    CreateFileRequest,
)
from helenite.master import master_pb2_grpc


class MasterServicer(master_pb2_grpc.MasterServicer):
    def __init__(self) -> None:
        pass

    def CreateFile(self, request: CreateFileRequest, context) -> bool:
        return super().CreateFile(request, context)

    def AllocateChunk(self, request: AllocateChunkRequest, context):
        return super().AllocateChunk(request, context)

    def GetChunkInformation(self, request: ChunkHandle, context) -> ChunkInformation:
        return super().GetChunkInformation(request, context)


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
