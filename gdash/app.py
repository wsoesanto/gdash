import json
import os
import sys
import urlparse

import requests
from flask import Flask, render_template, request

import globalvars
from api.dirlayout import app as api_dirlayout_blueprint
from api.volume import app as api_volume_blueprint
from api.volumes import app as api_volumes_blueprint
from jinjahelper import JinjaHelper

app = Flask(__name__)


@app.route("/")
@app.route("/volume/<vol_name>")
def index(vol_name=None):
    return render_template("index.html")


@app.route("/volume/<vol_name>/bricks/range/dir-tree", methods=["POST"])
def get_jquery_file_tree(vol_name):
    dir_path = request.form["dir"]
    hostname = "0.0.0.0"
    port = globalvars.args.port
    # Do the HTTP GET to itself
    url_scheme = {
        "scheme": "http",
        "netloc": "%s:%s" % (hostname, port),
        "path": "/api/volume/%s/bricks/range" % vol_name,
        "params": "",
        "query": "",
        "fragment": ""
    }
    url = urlparse.urlunparse(urlparse.ParseResult(**url_scheme))
    res = requests.get(url)
    if res.content == "Error":
        return "Cannot read brick layout"
    data = json.loads(res.content)
    return JinjaHelper.file_tree_list(dir_path, "root", data)


if __name__ == "__main__":
    if os.getuid() != 0:
        sys.stderr.write("Only root can run this\n")
        sys.exit(1)

    globalvars.init()

    # Threaded must be activated since possibility of self request in getting brick range
    app.jinja_env.globals.update(helper=JinjaHelper)
    app.register_blueprint(api_volumes_blueprint)
    app.register_blueprint(api_volume_blueprint)
    app.register_blueprint(api_dirlayout_blueprint)
    app.run(host='0.0.0.0', debug=globalvars.args.debug, port=globalvars.args.port, threaded=True)
