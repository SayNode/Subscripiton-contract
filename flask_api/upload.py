from msilib.schema import Class
from flask import Flask, json, request, jsonify, render_template, redirect, url_for

# from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
import os
from os.path import join, dirname, realpath
import urllib.request
import werkzeug
from werkzeug.utils import secure_filename
import os

"""
with open(join(dirname(realpath(__file__)), "/entrust_2048_ca.cer"), "r") as file:
    data = file.read()
x509 = crypto.load_certificate(crypto.FILETYPE_PEM, data)
p12 = crypto.PKCS12()
p12.set_certificate(x509)

context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_certificate("entrust_2048_ca.crt")
context.use_privatekey("server.key")

"""

app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), "static/uploads/..")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set([".xlsx", "pdf", "pptx"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


Files = {}

api = Api(app)


class Main(Resource):
    def get(self):
        return "Hello"


api.add_resource(Main, "/")

''' def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "file", type=werkzeug.datastructures.FileStorage, location="files"
        )
        """self.reqparse.add_argument("lat", type=float, default="")
        self.reqparse.add_argument("lon", type=float, default="")"""
        super(uploadPhoto, self).__init__()'''


class uploadImage(Resource):
    def post(self):
        file = request.files["file"]
        if file and allowed_file(file.filename):
            # From flask uploading tutorial
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("uploadimage", filename=filename))
        else:
            # return error
            return {"False"}


api.add_resource(uploadImage, "/upload")


if __name__ == "__main__":
    app.run(ssl_context=("cert.pem", "key.pem"))
    # app.run(debug=True, ssl_context=context, port=4000)
    # app.run(debug=True)

# To run it download a test rest api app, I used the extenstion Advanced Rest Client.
# Method: post
# Request URL:  http://127.0.0.1:5000/upload
# Header: Header name: Content-Type
#         Header value: multipart/form-data
# Body:
# Field name: files[] and the Choose the file you want to upload


# NOW POSSIBLE FROM THE WEB INTERFACE
