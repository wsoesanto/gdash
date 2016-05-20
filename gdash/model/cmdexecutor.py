import subprocess


class CmdExecutor:
    def __init__(self, is_debug=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE, env=None, close_fds=True):
        self.is_debug = is_debug
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.env = env
        self.close_fds = close_fds

    def execute(self, cmd):
        p = subprocess.Popen(cmd,
                             stdin=self.stdin,
                             stdout=self.stdout,
                             stderr=self.stderr,
                             env=self.env,
                             close_fds=self.close_fds)
        (out, err) = p.communicate()
        if self.is_debug:
            print("%s: %d" % (' '.join(cmd), p.returncode))
            if out:
                print("[Output]")
                print(out)
            if err:
                print("[Error]")
                print(err)
        return out
