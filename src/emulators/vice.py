import subprocess
import os

class Vice:
    def __init__(self, vice_bin="x64sc"):
        self.vice_bin = vice_bin

    def run(self, prg_file, debug=False, monitor_port=6502):
        if not os.path.exists(prg_file):
            return False, f"File not found: {prg_file}"

        cmd = [self.vice_bin]

        if debug:
            cmd.extend(["-remotemonitor", "-remotemonitoraddress", f"127.0.0.1:{monitor_port}"])

        cmd.append(prg_file)

        try:
            # We use Popen because we don't want to wait for VICE to close
            subprocess.Popen(cmd)
            return True, f"VICE started {'in debug mode' if debug else ''}"
        except Exception as e:
            return False, str(e)
