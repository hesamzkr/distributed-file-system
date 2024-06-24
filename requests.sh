curl -X POST -H "Content-Type: application/json" -d '{"filename": "testfile.txt", "size": 1024}' http://localhost:8080/create_file
curl -X POST -H "Content-Type: application/json" -d '{"filename": "testfile.txt"}' http://localhost:8080/delete_file
curl -X POST -H "Content-Type: application/json" -d '{"filename": "testfile.txt", "sequence_number": 1}' http://localhost:8080/allocate_chunk
curl -X POST -H "Content-Type: application/json" -d '{"handle": "chunk_handle_123"}' http://localhost:8080/get_chunk_information
