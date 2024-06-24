from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateFileRequest(_message.Message):
    __slots__ = ("filename", "size")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    filename: str
    size: int
    def __init__(self, filename: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...

class AllocateChunkRequest(_message.Message):
    __slots__ = ("filename", "sequenceNumber")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SEQUENCENUMBER_FIELD_NUMBER: _ClassVar[int]
    filename: str
    sequenceNumber: int
    def __init__(self, filename: _Optional[str] = ..., sequenceNumber: _Optional[int] = ...) -> None: ...

class ChunkHandle(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: str
    def __init__(self, handle: _Optional[str] = ...) -> None: ...

class ChunkInformation(_message.Message):
    __slots__ = ("handle", "servers")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    SERVERS_FIELD_NUMBER: _ClassVar[int]
    handle: str
    servers: _containers.RepeatedCompositeFieldContainer[ChunkServerAddress]
    def __init__(self, handle: _Optional[str] = ..., servers: _Optional[_Iterable[_Union[ChunkServerAddress, _Mapping]]] = ...) -> None: ...

class ChunkData(_message.Message):
    __slots__ = ("filename", "handle", "data")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    filename: str
    handle: str
    data: bytes
    def __init__(self, filename: _Optional[str] = ..., handle: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class ChunkServerAddress(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    def __init__(self, address: _Optional[str] = ...) -> None: ...

class FileInfo(_message.Message):
    __slots__ = ("chunks",)
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    chunks: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chunks: _Optional[_Iterable[str]] = ...) -> None: ...
