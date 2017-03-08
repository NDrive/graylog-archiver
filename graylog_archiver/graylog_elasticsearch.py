import os
import time

from graylog_archiver import utils


class GraylogElasticsearch:
    def __init__(self, es, max_indices, backup_dir):
        self.es = es
        self.max_indices = max_indices
        self.backup_dir = backup_dir

    def indices(self):
        return list(self.es.indices.get_mapping().keys())

    def indices_to_archive(self):
        indices_sorted = sorted(self.indices(), reverse=True)
        return indices_sorted[self.max_indices:]

    def create_backup_repository(self, location):
        repository = utils.random_string()

        self.es.snapshot.create_repository(
            repository,
            {
                "type": "fs",
                "settings": {
                    "location": location,
                    "compress": True
                }
            }

        )
        return repository

    def snapshot_is_done(self, repository, snapshot):
        response = self.es.snapshot.status(repository, snapshot)
        return response["snapshots"][0]["state"] == "SUCCESS"

    def dump(self, index):
        location = os.path.join(self.backup_dir, index)
        repository = self.create_backup_repository(location)

        self.es.snapshot.create(
            repository,
            "snapshot",
            {"indices": index}
        )

        while not self.snapshot_is_done(repository, "snapshot"):
            time.sleep(1)

        self.es.snapshot.delete_repository(repository)

        return location
