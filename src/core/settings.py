import json
import os

class Settings:
    def __init__(self):
        self.settings_file = os.path.expanduser("~/.c64studiopy.json")
        self.data = {
            "kickass_jar": "",
            "vice_bin": "",
            "last_project": ""
        }
        self.load()

    def load(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    self.data.update(json.load(f))
            except:
                pass

    def save(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
