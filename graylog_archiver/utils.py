import uuid
from shutil import make_archive
import os


def random_string():
    return "".join(str(uuid.uuid4()).split("-"))


def compress_directory(path):
    return make_archive(path, 'gztar', path)
