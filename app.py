import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


target = os.path.join(APP_ROOT, 'images/')


@app.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        imgdata = base64.b64decode(file)
        with open(filename, 'wb') as f:
            f.write(imgdata)
        destination = "/".join([target, filename])
        imgdata.save(destination)
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        # os.remove(os.path.join(target, filename))
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
