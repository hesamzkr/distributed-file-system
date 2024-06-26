import asyncio
import logging
import os
import socket

import grpc
from google.protobuf.empty_pb2 import Empty
from google.protobuf.wrappers_pb2 import BoolValue, BytesValue, StringValue
from grpc import ServicerContext

from helenite.chunkserver import config
from helenite.core import core_pb2_grpc
from helenite.core.core_pb2 import (
    ChunkData,
    ChunkHandle,
    ChunkInformation,
    ChunkServerAddress,
)


class ChunkServer(core_pb2_grpc.ChunkServerServicer):
    def __init__(self) -> None:
        self.channel = grpc.aio.insecure_channel(config.MASTER_ADDRESS)
        self.stub = core_pb2_grpc.MasterStub(self.channel)

        self.my_address = self.get_container_ip()
        logging.info(f"My Address: {self.my_address}")

        asyncio.create_task(self.RegisterChunkServer())

    def get_container_ip(self):
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    async def RegisterChunkServer(self) -> Empty:
        retry_count = 3

        while retry_count > 0:
            # Wait some time at the beginning
            await asyncio.sleep(5.0)

            try:
                await self.stub.RegisterChunkServer(ChunkServerAddress(address=self.my_address))
                logging.info(
                    f"Registered chunk server with master at address {config.MASTER_ADDRESS}"
                )
                break
            except Exception as e:
                logging.error(f"Error registering chunk server: {e}")
                retry_count -= 1

    async def Heartbeat(self, request: Empty, context: ServicerContext) -> Empty:
        logging.info("Received heartbeat from chunkserver")
        return Empty()

    async def write_chunk(
        self, request: ChunkData, context: ServicerContext
    ) -> ChunkInformation | None:
        info = await self.stub.GetChunkInformation(StringValue(value=request.handle))

        if self.my_address not in [server.address for server in info.servers]:
            logging.error(
                "Probably someone is trying to write a chunk to a chunk server where it is not supposed to be"
            )
            context.abort(
                grpc.StatusCode.NOT_FOUND, "Chunk server not in chunk information"
            )
            return

        try:
            # TODO: Remove this shit (create the folders)
            os.makedirs(
                os.path.join(config.NAMESPACE_DIR, request.filename), exist_ok=True
            )
            os.makedirs(config.CHUNKS_DIR, exist_ok=True)

            # Write the chunk to disk
            chunk_path = os.path.join(
                config.NAMESPACE_DIR, request.filename, request.handle
            )

            with open(chunk_path, "wb") as f:
                f.write(request.data)
            os.symlink(chunk_path, os.path.join(config.CHUNKS_DIR, request.handle))
            return info
        except Exception as e:
            logging.error(f"Error writing chunk to disk: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Error writing chunk to disk")

            return None

    async def ReplicateChunk(
        self, request: ChunkData, context: ServicerContext
    ) -> BoolValue:
        info = await self.write_chunk(request, context)

        if not info:
            return BoolValue(value=False)

        return BoolValue(value=True)

    async def WriteChunk(self, request: ChunkData, context: ServicerContext):
        info = await self.write_chunk(request, context)

        if not info:
            return BoolValue(value=False)

        # Replicate the chunk to other chunk servers
        for server in info.servers:
            if server.address == self.my_address:
                continue

            try:
                async with grpc.aio.insecure_channel(server.address) as channel:
                    stub = core_pb2_grpc.ChunkServerStub(channel)
                    await stub.ReplicateChunk(request)
            except Exception as e:
                logging.error(f"Error replicating chunk: {e}")
                return BoolValue(value=False)

        return BoolValue(value=True)

    async def ReadChunk(
        self, request: ChunkHandle, context: ServicerContext
    ) -> BytesValue:
        chunk_path = os.path.join(config.CHUNKS_DIR, request.handle)

        try:
            with open(chunk_path, "rb") as f:
                data = f.read()
            return BytesValue(value=data)
        except FileNotFoundError:
            context.abort(grpc.StatusCode.NOT_FOUND, "Chunk not found")

        return BytesValue()

    async def DeleteFile(
        self, request: StringValue, context: ServicerContext
    ) -> BoolValue:
        file_dir = os.path.join(config.NAMESPACE_DIR, request.value)

        if not os.path.exists(file_dir):
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")
            return

        # TODO: This can leave the file in an inconsistent state if it fails
        # We should create some garbage collection mechanism to handle it
        # EXAMPLE:
        # 1. If the file is deleted from the namespace but not from the chunks directory
        # 2. If some chunks are deleted but not all

        try:
            for chunk in os.listdir(file_dir):
                chunk_path = os.path.join(file_dir, chunk)

                os.remove(chunk_path)  # Remove the chunk
                os.unlink(os.path.join(config.CHUNKS_DIR, chunk))  # Remove the symlink

            # Remove the directory
            os.rmdir(file_dir)
            return BoolValue(value=True)
        except Exception as e:
            logging.error(f"Error deleting file: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Error deleting file")
            return BoolValue(value=False)


async def serve() -> None:
    server = grpc.aio.server()
    core_pb2_grpc.add_ChunkServerServicer_to_server(ChunkServer(), server)
    server.add_insecure_port("[::]:50052")
    logging.info("Starting server on port 50052")

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    asyncio.run(serve())
