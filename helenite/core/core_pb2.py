# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: helenite/core/core.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18helenite/core/core.proto\x12\rhelenite.core\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1bgoogle/protobuf/empty.proto\"3\n\x11\x43reateFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x03\"@\n\x14\x41llocateChunkRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x16\n\x0esequenceNumber\x18\x02 \x01(\x03\"\x1d\n\x0b\x43hunkHandle\x12\x0e\n\x06handle\x18\x01 \x01(\t\"r\n\x10\x43hunkInformation\x12*\n\x06handle\x18\x01 \x01(\x0b\x32\x1a.helenite.core.ChunkHandle\x12\x32\n\x07servers\x18\x02 \x03(\x0b\x32!.helenite.core.ChunkServerAddress\"%\n\x12\x43hunkServerAddress\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t2\xc9\x04\n\x06Master\x12L\n\nCreateFile\x12 .helenite.core.CreateFileRequest\x1a\x1a.google.protobuf.BoolValue\"\x00\x12H\n\nDeleteFile\x12\x1c.google.protobuf.StringValue\x1a\x1a.google.protobuf.BoolValue\"\x00\x12J\n\x0bGetFileSize\x12\x1c.google.protobuf.StringValue\x1a\x1b.google.protobuf.Int64Value\"\x00\x12W\n\rAllocateChunk\x12#.helenite.core.AllocateChunkRequest\x1a\x1f.helenite.core.ChunkInformation\"\x00\x12T\n\x13GetChunkInformation\x12\x1a.helenite.core.ChunkHandle\x1a\x1f.helenite.core.ChunkInformation\"\x00\x12V\n\x13RegisterChunkServer\x12!.helenite.core.ChunkServerAddress\x1a\x1a.google.protobuf.BoolValue\"\x00\x12T\n\x15UnregisterChunkServer\x12!.helenite.core.ChunkServerAddress\x1a\x16.google.protobuf.Empty\"\x00\x32L\n\x0b\x43hunkServer\x12=\n\tHeartbeat\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'helenite.core.core_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREATEFILEREQUEST']._serialized_start=104
  _globals['_CREATEFILEREQUEST']._serialized_end=155
  _globals['_ALLOCATECHUNKREQUEST']._serialized_start=157
  _globals['_ALLOCATECHUNKREQUEST']._serialized_end=221
  _globals['_CHUNKHANDLE']._serialized_start=223
  _globals['_CHUNKHANDLE']._serialized_end=252
  _globals['_CHUNKINFORMATION']._serialized_start=254
  _globals['_CHUNKINFORMATION']._serialized_end=368
  _globals['_CHUNKSERVERADDRESS']._serialized_start=370
  _globals['_CHUNKSERVERADDRESS']._serialized_end=407
  _globals['_MASTER']._serialized_start=410
  _globals['_MASTER']._serialized_end=995
  _globals['_CHUNKSERVER']._serialized_start=997
  _globals['_CHUNKSERVER']._serialized_end=1073
# @@protoc_insertion_point(module_scope)
