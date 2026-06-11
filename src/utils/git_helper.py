import subprocess
import os

class GitHelper:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def _run_git(self, args):
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout, result.stderr, result.returncode == 0
        except Exception as e:
            return "", str(e), False

    def status(self):
        return self._run_git(["status", "--short"])

    def branch(self):
        stdout, _, _ = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        return stdout.strip()

    def add(self, files):
        if isinstance(files, str):
            files = [files]
        return self._run_git(["add"] + files)

    def commit(self, message):
        return self._run_git(["commit", "-m", message])

    def push(self):
        return self._run_git(["push"])

    def pull(self):
        return self._run_git(["pull"])
