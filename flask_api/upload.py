from distutils.command.upload import upload
from flask import Flask, json, request, jsonify, render_template
import os
from os.path import join, dirname, realpath
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = join(dirname(realpath(__file__)), "static/uploads/..")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def main():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    # check if the post request has the file part
    if "files[]" not in request.files:
        resp = jsonify({"message": "No file part in the request"})
        resp.status_code = 400
        return resp

    files = request.files.getlist("files[]")

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            success = True
        else:
            errors[file.filename] = "File type is not allowed"

    if success and errors:
        errors["message"] = "File(s) successfully uploaded"
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({"message": "Files successfully uploaded"})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


if __name__ == "__main__":
    app.run(debug=True)

# To run it download a test rest api app, I used the extenstion Advanced Rest Client.
# Method: post
# Request URL:  http://127.0.0.1:5000/upload
# Header: Header name: Content-Type
#         Header value: multipart/form-data
# Body:
# Field name: files[] and the Choose the file you want to upload


# NOW POSSIBLE FROM THE WEB INTERFACE
