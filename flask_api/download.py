from flask import Flask, send_file, render_template
from os.path import join, dirname, realpath

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "download.html"
    )  # take the html file to show the download button


@app.route("/download")
def download_files():
    path = join(
        dirname(realpath(__file__)), "static/uploads/screenshot.png"
    )  # path to the file we want to download
    return send_file(path, as_attachment=True)  # download as an atachment


if __name__ == "__main__":
    app.run(debug=True)


# to download a file we run: http://127.0.0.1:5000/download and the file will be downloaded or http://127.0.0.1:5000/ and the download button

# to do: find a way to download specific files that are uploaded from the the ulpoad.py file without needed to write a function for each
