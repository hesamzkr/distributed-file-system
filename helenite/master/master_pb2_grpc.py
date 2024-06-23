# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from helenite.core import core_pb2 as helenite_dot_core_dot_core__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in helenite/master/master_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class MasterStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateFile = channel.unary_unary(
                '/helenite.master.Master/CreateFile',
                request_serializer=helenite_dot_core_dot_core__pb2.CreateFileRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_wrappers__pb2.BoolValue.FromString,
                _registered_method=True)
        self.AllocateChunk = channel.unary_unary(
                '/helenite.master.Master/AllocateChunk',
                request_serializer=helenite_dot_core_dot_core__pb2.AllocateChunkRequest.SerializeToString,
                response_deserializer=helenite_dot_core_dot_core__pb2.ChunkInformation.FromString,
                _registered_method=True)
        self.GetChunkInformation = channel.unary_unary(
                '/helenite.master.Master/GetChunkInformation',
                request_serializer=helenite_dot_core_dot_core__pb2.ChunkHandle.SerializeToString,
                response_deserializer=helenite_dot_core_dot_core__pb2.ChunkInformation.FromString,
                _registered_method=True)


class MasterServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AllocateChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetChunkInformation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateFile,
                    request_deserializer=helenite_dot_core_dot_core__pb2.CreateFileRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_wrappers__pb2.BoolValue.SerializeToString,
            ),
            'AllocateChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.AllocateChunk,
                    request_deserializer=helenite_dot_core_dot_core__pb2.AllocateChunkRequest.FromString,
                    response_serializer=helenite_dot_core_dot_core__pb2.ChunkInformation.SerializeToString,
            ),
            'GetChunkInformation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetChunkInformation,
                    request_deserializer=helenite_dot_core_dot_core__pb2.ChunkHandle.FromString,
                    response_serializer=helenite_dot_core_dot_core__pb2.ChunkInformation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'helenite.master.Master', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('helenite.master.Master', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Master(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/helenite.master.Master/CreateFile',
            helenite_dot_core_dot_core__pb2.CreateFileRequest.SerializeToString,
            google_dot_protobuf_dot_wrappers__pb2.BoolValue.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AllocateChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/helenite.master.Master/AllocateChunk',
            helenite_dot_core_dot_core__pb2.AllocateChunkRequest.SerializeToString,
            helenite_dot_core_dot_core__pb2.ChunkInformation.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetChunkInformation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/helenite.master.Master/GetChunkInformation',
            helenite_dot_core_dot_core__pb2.ChunkHandle.SerializeToString,
            helenite_dot_core_dot_core__pb2.ChunkInformation.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)