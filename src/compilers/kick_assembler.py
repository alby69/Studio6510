import subprocess
import os

class KickAssembler:
    def __init__(self, jar_path="KickAss.jar"):
        self.jar_path = jar_path

    def compile(self, source_file, output_dir=None):
        if output_dir is None:
            output_dir = os.path.dirname(source_file)

        # Command: java -jar KickAss.jar source.asm -odir output_dir
        cmd = ["java", "-jar", self.jar_path, source_file, "-odir", output_dir]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(cmd)
            }
        except Exception as e:
            return {
                "success": False,
                "stderr": str(e),
                "command": " ".join(cmd)
            }
