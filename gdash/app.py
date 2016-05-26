import os
import sys

from flask import Flask, render_template

import globalvars
from api.dirlayout import app as api_dirlayout_blueprint
from api.volume import app as api_volume_blueprint
from api.volumes import app as api_volumes_blueprint

app = Flask(__name__)


@app.route("/")
@app.route("/volume/<vol_name>")
def index(vol_name=None):
    return render_template("index.html")


if __name__ == "__main__":
    if os.getuid() != 0:
        sys.stderr.write("Only root can run this\n")
        sys.exit(1)

    globalvars.init()

    app.register_blueprint(api_volumes_blueprint)
    app.register_blueprint(api_volume_blueprint)
    app.register_blueprint(api_dirlayout_blueprint)

    # Threaded must be activated since possibility of self request in getting brick range
    app.run(host='0.0.0.0', debug=globalvars.args.debug, port=globalvars.args.port, threaded=True)
