import json
from xml.etree import cElementTree as ElementTree

from flask import Blueprint, Response

import globalvars
from model.glusteropt import VolumeStatusOption
from model.volume import Volume

app = Blueprint("api_volumes", __name__, url_prefix='/api')


@app.route("/volumes")
def get_volumes():
    cmd = globalvars.cmd
    executor = globalvars.executor
    volume_cmd = cmd.get_volume_command()
    res = executor.execute(volume_cmd.get_info())
    root = ElementTree.fromstring(res)
    volumes_xml = root.find("volInfo").find("volumes").findall("volume")

    volumes = list()
    for volume_xml in volumes_xml:
        volume = None
        volume_info = Volume.with_volume_info(volume_xml)
        # Check whether the volume is up or not
        if volume_info.status:
            volume_cmd = cmd.get_volume_command().get_volume(volume_info.name).get_status(VolumeStatusOption.DETAIL)
            res = executor.execute(volume_cmd)
            root = ElementTree.fromstring(res)
            volume_xml = root.find("volStatus").find("volumes").find("volume")
            volume_status = Volume.with_volume_status(volume_xml)
            volume = Volume.merge(volume_status, volume_info)
        else:
            volume = volume_info
        volumes.append(volume)

    return Response(
        response=json.dumps(volumes, default=Volume.to_json),
        mimetype="application/json"
    )


@app.route("/volumes/status")
def get_volumes_status():
    cmd = globalvars.cmd
    executor = globalvars.executor
    volume_cmd = cmd.get_volume_command()
    res = executor.execute(volume_cmd.get_status(VolumeStatusOption.DETAIL))
    root = ElementTree.fromstring(res)
    volumes_xml = root.find("volStatus").find("volumes").findall("volume")
    volumes = list()
    for volume_xml in volumes_xml:
        volume = Volume.with_volume_status(volume_xml)
        volumes.append(volume)

    return Response(
        response=json.dumps(volumes, default=Volume.to_json),
        mimetype="application/json"
    )
