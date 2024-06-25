import asyncio
import logging
import random
import uuid

import grpc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from google.protobuf.empty_pb2 import Empty
from google.protobuf.wrappers_pb2 import BoolValue, Int64Value, StringValue
from redis.asyncio import Redis

from helenite.core import core_pb2_grpc
from helenite.core.core_pb2 import (
    AllocateChunkRequest,
    ChunkHandle,
    ChunkInformation,
    ChunkServerAddress,
    CreateFileRequest,
    FileInfo,
)
from helenite.master import config

scheduler = AsyncIOScheduler()


class MasterServicer(core_pb2_grpc.MasterServicer):
    def __init__(self) -> None:
        self.redis = Redis.from_url(config.REDIS_URL, decode_responses=True)
        self.chunkservers = set()
        # self.chunks_to_delete = asyncio.Queue()
        self.files_to_delete = asyncio.Queue()  # optimized for O(1) deletion

        # Locks
        self.delete_lock = asyncio.Lock()
        self.chunkservers_lock = asyncio.Lock()

        # Register the scheduler to run every 60 seconds
        # and check if are still alive and woking
        scheduler.add_job(self.check_chunkservers, "interval", seconds=60)
        scheduler.add_job(self.garbage_collector, "interval", seconds=60)

    async def CreateFile(
        self, request: CreateFileRequest, context: grpc.ServicerContext
    ) -> BoolValue:
        async with self.redis.pipeline() as pipe:
            if await pipe.exists(f"file:{request.filename}"):
                await pipe.delete(f"file:{request.filename}")

                # Delete it right now
                await self.delete_file(request.filename)
            await pipe.hset(f"file:{request.filename}", mapping={"size": request.size})
            await pipe.execute()

        return BoolValue(value=True)

    async def DeleteFile(
        self, request: StringValue, context: grpc.ServicerContext
    ) -> BoolValue:
        filename = request.value

        async with self.redis.pipeline() as pipe:
            if await pipe.exists(f"file:{filename}"):
                await pipe.delete(f"file:{filename}")
                async with self.delete_lock:
                    await self.files_to_delete.put(filename)
                return BoolValue(value=True)
            else:
                return BoolValue(value=False)

    async def GetFileInformation(
        self, request: StringValue, context: grpc.ServicerContext
    ):
        if request.value in self.files_to_delete:
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")
            return FileInfo(chunks=[])

        try:
            filename = request.value
            chunks = await self.redis.lrange(f"chunks:{filename}", 0, -1)
            size = int(await self.redis.hget(f"file:{request.value}", "size"))
            return FileInfo(size=size, chunks=chunks)
        except Exception as e:
            logging.error(f"Error getting file information: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Error getting all the chunks")
            return FileInfo(chunks=[])

    async def AllocateChunk(
        self, request: AllocateChunkRequest, context: grpc.ServicerContext
    ) -> ChunkInformation:
        if request.filename in self.files_to_delete or not await self.redis.exists(
            f"file:{request.filename}"
        ):
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")
            return ChunkInformation(handle="", servers=[])

        # Generate a random chunk handle and select random chunk servers
        handle = handle = uuid.uuid4().hex
        ret = random.sample(list(self.chunkservers), config.REPLICATION_FACTOR)

        # Add the chunk handle to the file
        await self.redis.lpush(f"chunks:{request.filename}", handle)
        await self.redis.lpush(f"servers:{handle}", *ret)

        return ChunkInformation(
            handle=handle,
            servers=[ChunkServerAddress(address=server) for server in ret],
        )

    async def GetChunkInformation(
        self, request: ChunkHandle, context: grpc.ServicerContext
    ) -> ChunkInformation:
        try:
            servers = await self.redis.lrange(f"servers:{request.handle}", 0, -1)
            return ChunkInformation(
                handle=request.handle,
                servers=[ChunkServerAddress(address=server) for server in servers],
            )
        except Exception as e:
            logging.error(f"Error getting chunk information: {e}")
            return ChunkInformation(handle=request, servers=[])

    async def RegisterChunkServer(
        self, request: ChunkServerAddress, context: grpc.ServicerContext
    ) -> BoolValue:
        async with self.chunkservers_lock:
            self.chunkservers.add(request.address)
        logging.info(f"Registered chunk server [{request.address}] successfully")
        return BoolValue(value=True)

    async def UnregisterChunkServer(
        self, request: ChunkServerAddress, context: grpc.ServicerContext
    ):
        try:
            async with self.chunkservers_lock:
                self.chunkservers.remove(request.address)
            logging.info(f"Unregistered chunk server [{request.address}] successfully")
        except KeyError:
            logging.error(
                f"Chunk server [{request.address}] trying to say good bye!!, \
                but it was not registered before."
            )
        return Empty()

    async def check_chunkservers(self):
        await self.chunkservers_lock.acquire()

        for server in self.chunkservers:
            try:
                address = f"{server}:50052"
                async with grpc.aio.insecure_channel(address) as channel:
                    stub = core_pb2_grpc.ChunkServerStub(channel)
                    await stub.Heartbeat(Empty())
            except Exception as e:
                logging.error(f"Chunk server {server} is not alive anymore: {e}")
                self.chunkservers.remove(server)

        self.chunkservers_lock.release()

    async def delete_file(self, filename: str):
        # Get all the servers that have the chunks of the file
        try:
            servers = set()
            chunks = await self.redis.lrange(f"chunks:{filename}", 0, -1)
            for chunk in chunks:
                servers.update(await self.redis.lrange(f"servers:{chunk}", 0, -1))

            # Send a delete request to all the servers
            # TODO: This is not optimal, we should send the delete request in parallel
            # to all the servers. This is just a simple implementation
            # NOTE: This is synchronous, in order to avoid inconsistencies
            for server in servers:
                address = f"{server}:50052"
                async with grpc.aio.insecure_channel(address) as channel:
                    stub = core_pb2_grpc.ChunkServerStub(channel)
                    await stub.DeleteFile(StringValue(value=filename))
        finally:
            await self.redis.delete(f"chunks:{filename}")
            await self.redis.delete(f"file:{filename}")

    async def garbage_collector(self):
        await self.delete_lock.acquire()

        while not self.files_to_delete.empty():
            filename = self.files_to_delete.get_nowait()
            try:
                await self.delete_file(filename)
            except Exception as e:
                await self.files_to_delete.put(filename)
                logging.error(
                    f"Error deleting file {filename}: {e}. Retrying in 60 seconds..."
                )

        self.delete_lock.release()


async def serve() -> None:
    server = grpc.aio.server()
    core_pb2_grpc.add_MasterServicer_to_server(MasterServicer(), server)
    server.add_insecure_port("[::]:50051")
    logging.info("Starting server on port 50051")

    scheduler.start()

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    asyncio.run(serve())
