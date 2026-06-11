import os
import yaml

class Project:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.files = []
        self.settings = {
            "assembler": "kickassembler",
            "emulator": "vice",
            "target": "c64"
        }

    def save(self):
        project_file = os.path.join(self.path, f"{self.name}.c64proj")
        data = {
            "name": self.name,
            "settings": self.settings,
            "files": self.files
        }
        with open(project_file, 'w') as f:
            yaml.dump(data, f)

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        project = cls(data['name'], os.path.dirname(filepath))
        project.settings = data.get('settings', project.settings)
        project.files = data.get('files', [])
        return project
