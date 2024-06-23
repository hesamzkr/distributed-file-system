# Helenite File System

A simple distributed file system similar to Google File System (GFS)

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
