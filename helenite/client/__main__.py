import grpc
from google.protobuf.wrappers_pb2 import StringValue, Int64Value, BoolValue
from google.protobuf.empty_pb2 import Empty
# import helenite_pb2
# import helenite_pb2_grpc
from helenite.core import core_pb2_grpc
from helenite.core.core_pb2 import (
    AllocateChunkRequest,
    ChunkHandle,
    ChunkInformation,
    ChunkServerAddress,
    CreateFileRequest,
)


class HeleniteClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.master_stub = core_pb2_grpc.MasterStub(self.channel)

    def create_file(self, filename, size):
        request = CreateFileRequest(filename=filename, size=size)
        response = self.master_stub.CreateFile(request)
        return response.value

    def delete_file(self, filename):
        request = StringValue(value=filename)
        response = self.master_stub.DeleteFile(request)
        return response.value

    def allocate_chunk(self, filename, sequence_number):
        request = AllocateChunkRequest(filename=filename, sequence_number=sequence_number)
        response = self.master_stub.AllocateChunk(request)
        return response

    def get_chunk_information(self, handle):
        request = ChunkHandle(handle=handle)
        response = self.master_stub.GetChunkInformation(request)
        return response


if __name__ == "__main__":
    # TODO need to do proper configuration
    client = HeleniteClient("localhost:50051")


    result = client.create_file("testfile.txt", 1024)
    print("CreateFile response:", result)


    result = client.delete_file("testfile.txt")
    print("DeleteFile response:", result)


    chunk_info = client.allocate_chunk("testfile.txt", 1)
    print("AllocateChunk response:", chunk_info)


    chunk_info = client.get_chunk_information("chunk_handle_123")
    print("GetChunkInformation response:", chunk_info)
