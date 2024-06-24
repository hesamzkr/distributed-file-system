import asyncio
import logging

import grpc

from helenite.core import core_pb2_grpc
from helenite.core.core_pb2 import AllocateChunkRequest, ChunkData, CreateFileRequest


async def main() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = core_pb2_grpc.MasterStub(channel)
        req = CreateFileRequest(filename="test.txt", size=2048)

        await stub.CreateFile(req)
        handle1 = await stub.AllocateChunk(AllocateChunkRequest(filename="test.txt"))
        handle2 = await stub.AllocateChunk(AllocateChunkRequest(filename="test.txt"))

    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = core_pb2_grpc.ChunkServerStub(channel)
        data1 = ChunkData(
            filename="test.txt",
            handle=handle1.handle,
            data=b"0" * 1024,
        )
        await stub.WriteChunk(data1)

        data2 = ChunkData(
            filename="test.txt",
            handle=handle2.handle,
            data=b"0" * 1024,
        )
        await stub.WriteChunk(data2)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
