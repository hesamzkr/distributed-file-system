# Helenite File System

A simple distributed file system similar to Google File System (GFS)

- [Architecture](#architecture)
  - [Master Node](#master-node)
  - [Chunk Servers](#chunk-servers)
  - [Client](#client)
- [Technologies Used](#technologies-used)
- [Project layout](#project-layout)
- [Development](#development)
  - [Installation](#installation)
  - [Generate Python Code](#generate-python-code)
- [How to Run](#how-to-run)

## Architecture

### Master Node

- Single point of failure in the system.
- Keeps track of all file chunks in the system.
- Using Redis and persistance stores the file names, the unique ID of all chunks, location of each chunk.
- Knows the status of all alive chunk servers by pinging them (heartbeat).

### Chunk Servers

- No resharding in case of failure or adding of new chunk servers.
- Store chunks of a file in the physical drive.
- Accept request from client to upload/download chunks.
- Gets info about other chunks from master node and does the replication.

### Client

- Asks master node to create a file with some size.
- Send file chunks to primary chunk server.
- Ask the master node for a file and get list of chunks.
- Cache the list of chunks for a file and download them from the chunk servers.

## Technologies Used

- Python
- Redis: For storing metadata on master node and client.
- gRPC: For communication between client, master node and chunk servers.

## Project layout

- `helenite`:

  The master, chunkserver, and client code is defined in `__main__.py` and each part of the system is treated as a python module. They all share the `core` module and use `config.py` to configure themselves based on the environment.

  - `core`: Core python code generated by gRPC tools from protobuf files which are shared between all parts of the system.
  - `master`: Implementation of the gRPC master service.
  - `chunkserver`: Implementation of the chunk server gRPC service.
  - `client`: Implementation of a FastAPI http client for ease of use which makes gRPC calls to the master node and chunkservers.

- `proto`: Defines all services and messages the system is using to communicate between nodes in Protobuf files.
- `tests`: Simple tests of the system.
- `Dockerfile`: Docker file which builds the environment & dependencies all parts of the system share.
- `docker-compose.yml`: Docker compose file which defines the configuration to use `Dockerfile` with different commands to run specific services. It also creates two redis containers, one for the client and one for the master node.
  It creates x replicas of chunkserver and can be configured.
- `.env.example`: Example environment variables required for the system to work.

## Development

### Installation

Firstly make sure to have [poetry](https://python-poetry.org/docs/#installation) package manager installed on your system.

Then:

```bash
poetry install
```

### Generate Python Code For gRPC

To generate python code from protobuf files, run the following command in the root directory of the project:

```bash
python -m grpc_tools.protoc -Iproto --python_out=. --pyi_out=. --grpc_python_out=. proto/helenite/*/*.proto
```

## How to Run

Copy the `.env.example` file contents to `.env`.

The number of chunk servers spinned up is configurable in the `docker-compose.yml` file under `services.chunkserver.deploy.replicas`

Run the docker compose configuration to start the system with:

```bash
docker compose up -d --build
```

This will start the following services:

- one client + redis for cache with port forwarding
- one master node port forwarded. Also on network with chunkservers and redis-master.
- x chunk servers depedning on the docker-compose.yml file

Open http://localhost:8000/docs to see the client API documentation.
Using the interactive documentation you can use the client to interact with the system.
