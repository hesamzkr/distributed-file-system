from flask import Flask, request, jsonify

from helenite.client.helenite_client import HeleniteClient

app = Flask(__name__)
# TODO from configuration
client = HeleniteClient("localhost:50051")


@app.route('/create_file', methods=['POST'])
def create_file():
    data = request.json
    filename = data.get('filename')
    size = data.get('size')
    if filename is None or size is None:
        return jsonify({"error": "Invalid input"}), 400
    result = client.create_file(filename, size)
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
    app.run(host='0.0.0.0', port=8080)
