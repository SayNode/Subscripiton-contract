from inspect import signature
from msilib.schema import Class
from flask import Flask, json, request, jsonify, render_template, redirect, url_for
import ipfshttpclient
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
import os
from os.path import join, dirname, realpath
import urllib.request
from werkzeug.utils import secure_filename
import os
import logging
from flask_script import Manager
import encryption

app = Flask(__name__)
CORS(app)
app.config.from_pyfile("config.py")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set([".xlsx", "pdf", "pptx"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


Files = {}
manager = Manager(app)

console = logging.StreamHandler()
root = logging.getLogger("")
root.addHandler(console)
api = Api(app, catch_all_404s=True)


class Main(Resource):
    def get(self):
        return "Hello"


api.add_resource(Main, "/")


class uploadFile(Resource):
    def post(self):
        try:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                logging.info("file name: {}".format(file.filename), {"app": "api"})
                client = ipfshttpclient.connect(app.config["IPFS_CONNECT_URL"])
                res = client.add(file)
                logging.info("upload res: {}".format(res), {"app": "upload"})
                url = str(app.config["DOMAIN"] + "/" + str(res["Hash"]))
                # return url
                encrypted_url = str(encryption.encrypt(url, encryption.pubKey))
                return encrypted_url
        except Exception as e:
            logging.exception("Upload Error! exception:{}".format(str(e)))
            return "Upload Error! \n", 503


api.add_resource(uploadFile, "/upload")


if __name__ == "__main__":
    # app.run(ssl_context=("cert.pem", "key.pem"))
    # app.run(debug=True, ssl_context=context, port=4000)
    app.run(debug=True)

# To run it download a test rest api app, I used Advanced Rest Client.
# Method: post
# Request URL:  http://127.0.0.1:5000/upload
# Header: Header name: Content-Type
#         Header value: multipart/form-data
# Body:
# Field name: <file> and then choose the file you want to upload


# NOW POSSIBLE FROM THE WEB INTERFACE
