import json

from flask import Blueprint, request, Response

from model.dirlayout import DirLayout
from model.util import get_dir_layout

app = Blueprint("api_dirlayout", __name__, url_prefix='/api')


@app.route("/dirlayout/get-range", methods=["POST"])
def get_range():
    # TODO: Handle if the path is not inserted
    path = request.form["path"]
    dir_layout = get_dir_layout(path)
    return Response(
        json.dumps(dir_layout, default=DirLayout.to_json),
        mimetype="application/json"
    )
