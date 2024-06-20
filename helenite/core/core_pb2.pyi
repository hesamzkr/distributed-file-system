from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateFileRequest(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class AllocateChunkRequest(_message.Message):
    __slots__ = ("path", "sequenceNumber")
    PATH_FIELD_NUMBER: _ClassVar[int]
    SEQUENCENUMBER_FIELD_NUMBER: _ClassVar[int]
    path: str
    sequenceNumber: int
    def __init__(self, path: _Optional[str] = ..., sequenceNumber: _Optional[int] = ...) -> None: ...

class BulkAllocateChunkRequest(_message.Message):
    __slots__ = ("path", "count")
    PATH_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    path: str
    count: int
    def __init__(self, path: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class ChunkHandle(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: str
    def __init__(self, handle: _Optional[str] = ...) -> None: ...

class ChunkInformation(_message.Message):
    __slots__ = ("handle", "primary", "secondaries")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_FIELD_NUMBER: _ClassVar[int]
    SECONDARIES_FIELD_NUMBER: _ClassVar[int]
    handle: ChunkHandle
    primary: str
    secondaries: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, handle: _Optional[_Union[ChunkHandle, _Mapping]] = ..., primary: _Optional[str] = ..., secondaries: _Optional[_Iterable[str]] = ...) -> None: ...
