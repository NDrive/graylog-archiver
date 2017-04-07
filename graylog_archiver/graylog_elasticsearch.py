import os
import time
import re

from graylog_archiver import utils


def extract_number(index):
    return int(re.findall(r'\d+', index)[0])


def sort_indices(indices):
    """Sort indices from the oldest"""
    return sorted(indices, key=extract_number)


class GraylogElasticsearch:
    def __init__(self, es, max_indices, backup_dir):
        self.es = es
        self.max_indices = max_indices
        self.backup_dir = backup_dir

    def indices(self):
        return list(self.es.indices.get_mapping().keys())

    def indices_to_archive(self):
        indices_sorted = sort_indices(self.indices())
        return indices_sorted[self.max_indices:]

    def create_backup_repository(self, repository, location):
        return self.es.snapshot.create_repository(
            repository,
            {
                "type": "fs",
                "settings": {
                    "location": location,
                    "compress": True
                }
            }

        )

    def snapshot_is_done(self, repository, snapshot):
        response = self.es.snapshot.status(repository, snapshot)
        return response["snapshots"][0]["state"] == "SUCCESS"

    def delete_index(self, index):
        return self.es.indices.delete(index)

    def dump(self, index):
        location = os.path.join(self.backup_dir, index)
        backup_repository = utils.random_string()

        self.create_backup_repository(backup_repository, location)
        self.es.snapshot.create(
            backup_repository,
            "snapshot",
            {"indices": index}
        )

        while not self.snapshot_is_done(backup_repository, "snapshot"):
            time.sleep(1)

        self.es.snapshot.delete_repository(backup_repository)

        return location
