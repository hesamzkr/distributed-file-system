from typing import Annotated

import grpc
import uvicorn
from fastapi import FastAPI, File, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from google.protobuf.wrappers_pb2 import StringValue

from helenite.client import config
from helenite.core import core_pb2_grpc
from helenite.core.core_pb2 import (
    AllocateChunkRequest,
    ChunkData,
    ChunkHandle,
    CreateFileRequest,
)

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
        for _ in range(file.size // 1024 + 1):
            req = AllocateChunkRequest(filename=file.filename)
            info = await stub.AllocateChunk(req)
            handlers.append(info)

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
    async with grpc.aio.insecure_channel(config.MASTER_ADDRESS) as channel:
        stub = core_pb2_grpc.MasterStub(channel)

        req = StringValue(value=filename)
        file_info = await stub.GetFileInformation(req)
        ret = []

        for chunk in file_info.chunks:
            info = await stub.GetChunkInformation(ChunkHandle(handle=chunk))
            ret.append((chunk, info.servers[0].address))

    async def iter_file():
        for chunk, address in ret:
            address = f"{address}:50052"
            async with grpc.aio.insecure_channel(address) as channel:
                stub = core_pb2_grpc.ChunkServerStub(channel)

                data = await stub.ReadChunk(ChunkHandle(handle=chunk))
                print(data.value)
                yield data.value

    return StreamingResponse(
        iter_file(), media_type="application/octet-stream", status_code=status.HTTP_200_OK
    )


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
