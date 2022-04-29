from flask import Flask, send_file, render_template

app = Flask(__name__)


@app.route("/")
def home():
    pass


@app.route("/download")
def download_files():
    path = "static/uploads/screenshot.png"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)


# to download a file we run: http://127.0.0.1:5000/download and the file will be downloaded

# to do: find a way to download specific files that are uploaded from the the ulpoad.py file without needed to write a function for each
