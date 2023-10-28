"""
Omnipotent
"""

__version__ = "322"

import os
from dataclasses import dataclass
from subprocess import run

from flask import Flask, flash, redirect, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"html"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@dataclass
class SearchResult:
    title: str


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/search")
def search():
    results = run(
        [
            "rga",
            "--rga-adapters=pandoc",
            "--files-with-matches",
            "--null",
            request.args.get("query", ""),
        ],
        capture_output=True,
        cwd="uploads",
        text=True,
        check=False,
    ).stdout.split("\0")
    print(results)
    return render_template("search.html", results=results)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    after_upload = False

    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            after_upload = True

    return render_template("index.html", after_upload=after_upload)
