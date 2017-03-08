import uuid
import invoke


def random_string():
    return "".join(str(uuid.uuid4()).split("-"))


def compress_directory(path):
    cmd = "tar czvf {0}.tar.gz {0}".format(path)
    invoke.run(cmd, hide=True)
    return "{0}.tar.gz".format(path)
