import json
from typing import Annotated

import grpc
import uvicorn
from fastapi import FastAPI, File, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from google.protobuf.wrappers_pb2 import StringValue
from redis.asyncio import Redis

from helenite.client import config
from helenite.core import core_pb2_grpc
from helenite.core.core_pb2 import (
    AllocateChunkRequest,
    ChunkData,
    ChunkHandle,
    CreateFileRequest,
)

redis_client = Redis.from_url(config.REDIS_URL, decode_responses=True)

app = FastAPI(
    title="Helenite Client",
    version="1.0",
    description="",
)


@app.post("/create-file")
async def create_file(
    file: Annotated[UploadFile, File()],
):
    async with grpc.aio.insecure_channel(config.MASTER_ADDRESS) as channel:
        stub = core_pb2_grpc.MasterStub(channel)

        req = CreateFileRequest(filename=file.filename, size=file.size)
        await stub.CreateFile(req)

        handlers = []

        # allocate chunks for file
        num_chunks = file.size // 1024
        if file.size % 1024 != 0:
            num_chunks += 1
        for _ in range(num_chunks):
            req = AllocateChunkRequest(filename=file.filename)
            info = await stub.AllocateChunk(req)
            handlers.append(info)

        file_info = {
            "chunks": [
                {
                    "handle": handler.handle,
                    "servers": [server.address for server in handler.servers],
                }
                for handler in handlers
            ]
        }
        await redis_client.set(f"client:{file.filename}", json.dumps(file_info))

    p = 0
    while True:
        chunk = await file.read(1024)
        if not chunk:
            break

        handler = handlers[p]
        p += 1
        address = f"{handler.servers[0].address}:50052"
        async with grpc.aio.insecure_channel(address) as channel:
            stub = core_pb2_grpc.ChunkServerStub(channel)

            req = ChunkData(filename=file.filename, handle=handler.handle, data=chunk)
            await stub.WriteChunk(req)

    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/read-file/{filename}")
async def read_file(filename: str):
    # await redis_client.delete(filename)
    file_info = await redis_client.get(f"client:{filename}")
    if file_info:
        file_info_json = json.loads(file_info)
    else:
        async with grpc.aio.insecure_channel(config.MASTER_ADDRESS) as channel:
            stub = core_pb2_grpc.MasterStub(channel)

            req = StringValue(value=filename)
            file_info = await stub.GetFileInformation(req)
            file_info_json = {"chunks": []}

            for chunk in file_info.chunks:
                info = await stub.GetChunkInformation(ChunkHandle(handle=chunk))
                file_info_json["chunks"].append(
                    {
                        "handle": chunk,
                        "servers": [server.address for server in info.servers],
                    }
                )
            await redis_client.set(f"client:{filename}", json.dumps(file_info_json))

    async def iter_file():
        for chunk in file_info_json["chunks"]:
            address = f"{chunk['servers'][0]}:50052"
            async with grpc.aio.insecure_channel(address) as channel:
                stub = core_pb2_grpc.ChunkServerStub(channel)

                data = await stub.ReadChunk(ChunkHandle(handle=chunk["handle"]))
                yield data.value

    return StreamingResponse(
        iter_file(),
        media_type="application/octet-stream",
        status_code=status.HTTP_200_OK,
    )

@app.delete("/delete-file/{filename}")
async def delete_file(filename: str):
    async with grpc.aio.insecure_channel(config.MASTER_ADDRESS) as channel:
        stub = core_pb2_grpc.MasterStub(channel)

        req = StringValue(value=filename)
        await stub.DeleteFile(req)

    await redis_client.delete(f"client:{filename}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/get-file-info/{filename}")
async def get_file_info(filename: str):
    async with grpc.aio.insecure_channel(config.MASTER_ADDRESS) as channel:
        stub = core_pb2_grpc.MasterStub(channel)

        req = StringValue(value=filename)
        file_info = await stub.GetFileInformation(req)
        return {
            "filename": filename,
            "size": file_info.size,
            "chunks": len(file_info.chunks),
        }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
