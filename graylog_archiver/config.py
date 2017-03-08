import json
import os


DEFAULT_FILE = "graylog_archiver.json"


def default_configuration_file():
    dirs = [
        os.getcwd(),
        os.path.expanduser("~")
    ]
    for d in dirs:
        path = os.path.join(d, DEFAULT_FILE)
        if os.path.exists(path):
            return path
    return None


class Config:
    def __init__(self, path):
        f = open(path, "r")
        self.conf = json.load(f)
        f.close()

    def get(self, section):
        return self.conf[section]
