from flask import Flask, request, jsonify, send_from_directory
import os
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'uploads'
if not IMAGE_DIR.exists():
    IMAGE_DIR.mkdir()


@app.route('/', methods=['GET'])
def start():
    files_dict = dict()
    files = [file for file in IMAGE_DIR.iterdir() if file.is_file()]
    for order_number, file in enumerate(files, 1):
        files_dict[f"image_{order_number}"] = f"{request.host_url}image/{file.name}"
    return jsonify({'images_endpoints': files_dict})


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = os.path.join(IMAGE_DIR, image.filename)
    image.save(filename)

    return jsonify({'uploaded_image_static_url': request.host_url + 'uploads/' + image.filename}), 201


@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    content_type = request.headers.get('Content-Type')
    filepath = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(filepath):
        if content_type == 'text':
            return jsonify({'get_image_static_url': request.host_url + 'uploads/' + filename}), 200
        elif content_type == 'image' or 'image/*' in request.accept_mimetypes:
            return send_from_directory(IMAGE_DIR, filename)
        else:
            return jsonify({'error': 'Unsupported Content-Type'}), 400
    else:
        return jsonify({'error': 'Image not found'}), 404


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_image(filename):
    filepath = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Image not found'}), 404

    os.remove(filepath)
    return jsonify({'message': f'Image {filename} deleted'}), 200


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, port=port, debug=True)
