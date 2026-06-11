import subprocess
import os

class Vice:
    def __init__(self, vice_bin="x64sc"):
        self.vice_bin = vice_bin

    def run(self, prg_file):
        if not os.path.exists(prg_file):
            return False, f"File not found: {prg_file}"

        cmd = [self.vice_bin, prg_file]

        try:
            # We use Popen because we don't want to wait for VICE to close
            subprocess.Popen(cmd)
            return True, "VICE started"
        except Exception as e:
            return False, str(e)
