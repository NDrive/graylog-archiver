import subprocess
import logging

from elasticsearch import Elasticsearch


class Archiver:
    def __init__(self, config):
        self.config = config
        self.es = Elasticsearch(config.get("elasticsearch")["hosts"])
        self.max_indices = config.get("graylog")["max_indices"]
        self.backup_dir = config.get("backup")["directory"]
        self.rsync_args = config.get("backup")["rsync"]

    def indices(self):
        indices = self.es.search()["hits"]["hits"]
        indices = filter(lambda i: "graylog" in i["_index"], indices)
        return list(indices)

    def indices_to_delete(self):
        indices = self.indices()
        indices.sort(key=lambda i: i["_index"], reverse=True)
        filtered = indices[self.max_indices:]
        return list(map(lambda i: i["_index"], filtered))

    def repository_name(self, index):
        return "graylog_backup_repository_" + index

    def backup_path(self, index):
        return self.backup_dir + "/" + index

    def create_backup_repository(self, index):
        repository = self.repository_name(index)
        definition = {
            "type": "fs",
            "settings": {
                "location": self.backup_path(index),
                "compress": True
            }
        }
        self.es.snapshot.create_repository(repository, definition)

    def backup(self, index):
        repository = self.repository_name(index)
        snapshot = "snapshot"
        definition = {
            "indices": index,
            "ignore_unavailable": True,
            "include_global_state": False
        }
        self.es.snapshot.create(repository, snapshot, definition)

    def compress_backup(self, index):
        path = self.backup_path(index)
        cmd = "tar czvf {0}.tar.gz {0}".format(path)
        subprocess.run(cmd, shell=True, check=True)

    def rsync(self, index):
        path = "{0}.tar.gz".format(self.backup_path(index))
        cmd = "rsync {0} {1}".format(path, self.rsync_args)
        subprocess.run(cmd, shell=True, check=True)

    def delete_index(self, index):
        self.es.indices.delete(index)

    def delete_backup(self, index):
        path = self.backup_path(index)
        cmd = "rm -rf {0}.tar.gz {0}".format(path)
        subprocess.run(cmd, shell=True, check=True)

    def archive(self):
        indices_to_delete = self.indices_to_delete()
        logging.debug("Indices to delete: %s" % indices_to_delete)
        for index in indices_to_delete:
            self.create_backup_repository(index)
            self.backup(index)
            self.compress_backup(index)
            self.rsync(index)
            self.delete_index(index)
            self.delete_backup(index)
