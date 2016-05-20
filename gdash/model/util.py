import os
import struct
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import xattr

from dirlayout import DirLayout
from layout import Layout

PROG_DESCRIPTION = """
GlusterFS dashboard
-------------------

This tool is based on remote execution support provided by
GlusterFS cli for `volume info` and `volume status` commands
"""


def get_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description=PROG_DESCRIPTION)
    parser.add_argument('--port', '-p', help="Port", type=int, default=5000)
    parser.add_argument('--cache', '-c', help="Cache output in seconds",
                        type=int, default=5)
    parser.add_argument('--debug', help="DEBUG", action="store_true")
    parser.add_argument('--host',
                        help="Remote host which is part of cluster", default='localhost')
    parser.add_argument('--gluster',
                        help="If your gluster is not in /usr/sbin/gluster",
                        default='/usr/sbin/gluster')
    # default="/usr/sbin/gluster")

    print(parser.parse_args())
    return parser.parse_args()


def get_dir_layout(root_dir_path):
    dir_map = dict()
    for dir_path, dir_names, filenames in os.walk(root_dir_path):
        if len(dir_map) == 0:
            dir_map[dir_path] = DirLayout()  # Root folder
        else:
            par_dir_path = os.path.dirname(dir_path)
            par_dir_layout = dir_map[par_dir_path]

            # Create the subfolder
            dir_name = os.path.basename(dir_path)
            par_dir_layout.add_subfolder(dir_name)
            dir_map[dir_path] = par_dir_layout.get_subfolder(dir_name)
        dir_layout = dir_map[dir_path]

        # TODO: Ignore this part first. Figure out what to do with this folders
        if '.glusterfs' in dir_names:
            dir_names.remove('.glusterfs')
        if '.trashcan' in dir_names:
            dir_names.remove('.trashcan')

        ext_attr = xattr.getxattr(dir_path, 'trusted.glusterfs.dht')
        (dummy, start, end) = struct.unpack_from(">qII", ext_attr)
        dir_layout.set_layout(Layout(start, end))
    return dir_map[root_dir_path]


def main():
    print('hello')


if __name__ == "__main__":
    main()
