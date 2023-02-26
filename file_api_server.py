import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'No file provided'})

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'})

@app.route('/api/create-folder', methods=['POST'])
def create_folder():
    folder_name = request.json.get('name')
    if folder_name:
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], folder_name))
        return jsonify({'message': 'Folder created successfully'})
    else:
        return jsonify({'error': 'No folder name provided'})

@app.route('/api/list-files', methods=['GET'])
def list_files():
    dir_path = request.args.get('dir', '/')
    files = []
    for filename in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], dir_path)):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], dir_path, filename)
        if os.path.isfile(file_path):
            files.append(filename)
    return jsonify({'files': files})

@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'})

if __name__ == '__main__':
    app.run(debug=True)
