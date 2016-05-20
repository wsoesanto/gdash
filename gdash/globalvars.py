from model.cmdexecutor import CmdExecutor
from model.glustercmd import GlusterCommand
from model.util import get_args


def init():
    global args, cmd, executor
    args = get_args()
    cmd = GlusterCommand(args.gluster, args.host)
    executor = CmdExecutor()
