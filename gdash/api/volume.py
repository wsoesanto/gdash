import json
import urlparse
from xml.etree import cElementTree as ElementTree

import requests
from flask import Blueprint, Response

import globalvars
from model.dirlayout import DirLayout
from model.glusteropt import VolumeStatusOption
from model.mergeddirlayout import MergedDirLayout
from model.volume import Volume

app = Blueprint("api_volume", __name__, url_prefix='/api')


@app.route("/volume/<vol_name>")
def get_volume_info(vol_name):
    cmd = globalvars.cmd
    executor = globalvars.executor
    volume_cmd = cmd.get_volume_command().get_volume(vol_name)
    res = executor.execute(volume_cmd.get_info())
    root = ElementTree.fromstring(res)
    # TODO: When the 'vol_name' does not exist in gluster, gluster does not return error. Report it.
    volume_xml = root.find('volInfo').find('volumes').find('volume')
    volume_info = Volume.with_volume_info(volume_xml)

    if volume_info.status:
        volume_cmd = cmd.get_volume_command().get_volume(volume_info.name).get_status(VolumeStatusOption.DETAIL)
        res = executor.execute(volume_cmd)
        root = ElementTree.fromstring(res)
        volume_xml = root.find("volStatus").find("volumes").find("volume")
        volume_status = Volume.with_volume_status(volume_xml)
        volume = Volume.merge(volume_status, volume_info)
    else:
        volume = volume_info

    return Response(
        response=json.dumps(volume, default=Volume.to_json),
        mimetype="application/json"
    )


@app.route("/volume/<vol_name>/info")
def get_volume(vol_name):
    cmd = globalvars.cmd
    executor = globalvars.executor
    volume_cmd = cmd.get_volume_command().get_volume(vol_name)
    res = executor.execute(volume_cmd.info())
    root = ElementTree.fromstring(res)
    # TODO: When the 'vol_name' does not exist in gluster, gluster does not return error. Report it.
    volume_xml = root.find("volInfo").find("volumes").find("volume")
    volume = Volume.with_volume_info(volume_xml)
    return Response(
        response=json.dumps(volume, default=Volume.to_json),
        mimetype="application/json"
    )


@app.route("/volume/<vol_name>/start")
def start_volume(vol_name):
    cmd = globalvars.cmd
    executor = globalvars.executor
    volume_cmd = cmd.get_volume_command().get_volume(vol_name).start()
    res = executor.execute(volume_cmd)
    return res


@app.route("/volume/<vol_name>/stop")
def stop_volume(vol_name):
    cmd = globalvars.cmd
    executor = globalvars.executor
    volume_cmd = cmd.get_volume_command().get_volume(vol_name).stop()
    res = executor.execute(*volume_cmd)
    return res


@app.route("/volume/<vol_name>/bricks/range")
def get_ranges(vol_name):
    cmd = globalvars.cmd
    executor = globalvars.executor
    args = globalvars.args
    volume_cmd = cmd.get_volume_command().get_volume(vol_name)
    out_cmd = executor.execute(volume_cmd.get_status(VolumeStatusOption.DETAIL))
    root_xml = ElementTree.fromstring(out_cmd)

    if int(root_xml.find("opRet").text) != 0:
        # TODO: Handle when the volume does not exist
        return "Error"

    nodes_xml = root_xml.find("volStatus").find("volumes").find("volume").findall("node")
    dir_layouts = dict()
    for node_xml in nodes_xml:
        status = (int(node_xml.find("status").text) == 1)
        if not status:
            # TODO: The node/brick is off. Find out what is the difference between node and brick in this context
            continue

        hostname = node_xml.find("hostname").text
        port = args.port
        path = node_xml.find("path").text

        # Do the HTTP POST to get dir layout from each node
        url_scheme = {
            "scheme": "http",
            "netloc": "%s:%s" % (hostname, port),
            "path": "/api/dirlayout/get-range",
            "params": "",
            "query": "",
            "fragment": ""
        }

        url = urlparse.urlunparse(urlparse.ParseResult(**url_scheme))
        try:
            post_res = requests.post(url, data={"path": path})
            data = json.loads(post_res.content)
            brick_name = "{}:{}{}".format(hostname, port, path)
            dir_layouts[brick_name] = DirLayout.with_dir_layout_obj(data)
        except requests.exceptions.ConnectionError as e:
            print(e.message)

    layout_list = list()
    for brick_name, layout in dir_layouts.items():
        layout_list.append(layout)
    for idx, layout in enumerate(layout_list):
        if idx > 0:
            if layout != layout_list[idx - 1]:
                # TODO: Handle the case where the subfolder structure are not the same for each brick
                return "error"

    # Merge the layouts
    mergeddirlayout = MergedDirLayout(dir_layouts)
    return Response(
        response=json.dumps(mergeddirlayout, default=MergedDirLayout.to_json),
        mimetype="application/json"
    )
