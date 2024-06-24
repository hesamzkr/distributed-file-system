# Helenite File System

A simple distributed file system similar to Google File System (GFS)

- [Architecture](#architecture)
  - [Master Node](#master-node)
  - [Chunk Servers](#chunk-servers)
  - [Client](#client)
- [Installation](#installation)
- [Generate Python Code](#generate-python-code)

## Architecture

### Master Node

- Single point of failure in the system.
- Keeps track of all chunks in the system.
- Using Redis and persistance stores the file names, the unique ID of all chunks, location of each chunk.
- Knows the status of all alive chunk servers.

### Chunk Servers

- Static number of chunk servers.
- Store chunks of a file in the physical drive.
- Accept request from client to upload/download chunks.
- Gets info about other chunks from master node and does the replication.
- Send request to master node to tell it that it's alive.

### Client

- Asks master node to create a file with some size.
- Send file chunks to primary chunk server.
- Ask the master node for a file and get list of chunks.
- Cache the list of chunks for a file and download them from the chunk servers.

## Technologies Used

- Python
- Redis: For storing metadata on master node.
- gRPC: For communication between client, master node and chunk servers.

## Installation

To install the project, run the following command in the root directory of the project:

```bash
poetry install
```

## Generate Python Code

To generate python code from protobuf files, run the following command in the root directory of the project:

```bash
python -m grpc_tools.protoc -Iproto --python_out=. --pyi_out=. --grpc_python_out=. proto/helenite/*/*.proto
```
