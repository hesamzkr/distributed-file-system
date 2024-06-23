import logging

import grpc
from google.protobuf.wrappers_pb2 import StringValue

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

    def create_file(self, filename, size):
        request = CreateFileRequest(filename=filename, size=size)
        response = self.master_stub.CreateFile(request)
        logger.info(f"CreateFile response: {response.value}")
        return response.value

    def delete_file(self, filename):
        request = StringValue(value=filename)
        response = self.master_stub.DeleteFile(request)
        logger.info(f"DeleteFile response: {response.value}")
        return response.value

    def allocate_chunk(self, filename, sequence_number):
        request = AllocateChunkRequest(filename=filename, sequence_number=sequence_number)
        response = self.master_stub.AllocateChunk(request)
        logger.info(f"AllocateChunk response: {response}")
        return response

    def get_chunk_information(self, handle):
        request = ChunkHandle(handle=handle)
        response = self.master_stub.GetChunkInformation(request)
        logger.info(f"GetChunkInformation response: {response}")
        return response
