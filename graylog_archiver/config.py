import json


class Config:
    def __init__(self, path):
        f = open(path, "r")
        self.conf = json.load(f)
        f.close()

    def get(self, section):
        return self.conf[section]
