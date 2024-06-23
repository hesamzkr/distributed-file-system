from flask import Flask, request, jsonify
import os
import random
import string

from helenite.client.helenite_client import HeleniteClient

app = Flask(__name__)
# TODO from configuration
client = HeleniteClient("localhost:50051")


def generate_random_text_file(filename, size):
    with open(filename, 'w') as f:
        f.write(''.join(random.choices(string.ascii_letters + string.digits, k=size)))


def split_file_into_chunks(filename, chunk_size=1024):
    with open(filename, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk_number, chunk
            chunk_number += 1


@app.route('/create_file', methods=['POST'])
def create_file():
    data = request.json
    filename = data.get('filename')
    size = data.get('size')
    if filename is None or size is None:
        return jsonify({"error": "Invalid input"}), 400

    generate_random_text_file(filename, size)
    result = client.create_file(filename, size)
    for chunk_number, chunk in split_file_into_chunks(filename):
        client.allocate_chunk(filename, chunk_number)
    os.remove(filename)
    return jsonify({"result": result})


@app.route('/delete_file', methods=['POST'])
def delete_file():
    data = request.json
    filename = data.get('filename')
    if filename is None:
        return jsonify({"error": "Invalid input"}), 400
    result = client.delete_file(filename)
    return jsonify({"result": result})


@app.route('/allocate_chunk', methods=['POST'])
def allocate_chunk():
    data = request.json
    filename = data.get('filename')
    sequence_number = data.get('sequence_number')
    if filename is None or sequence_number is None:
        return jsonify({"error": "Invalid input"}), 400
    result = client.allocate_chunk(filename, sequence_number)
    return jsonify({"result": result})


@app.route('/get_chunk_information', methods=['POST'])
def get_chunk_information():
    data = request.json
    handle = data.get('handle')
    if handle is None:
        return jsonify({"error": "Invalid input"}), 400
    result = client.get_chunk_information(handle)
    return jsonify({"result": result})


if __name__ == "__main__":
    # TODO from configuration
    app.run(host='0.0.0.0', port=8080)
