import os
import time
import re
import shutil
from itertools import groupby, chain

from . import utils

INDEX_NAME_PATTERN = re.compile(r"(\S+)_\d+")


def extract_number(index):
    return int(re.findall(r'\d+', index)[0])


def sort_indices(indices):
    """Sort indices from the newest to oldest"""
    return sorted(indices, key=extract_number, reverse=True)


def group_and_sort_indices(indices):
    index_sets = [(re.match(INDEX_NAME_PATTERN, x).group(1), x) for x in indices if re.match(INDEX_NAME_PATTERN, x)]
    return dict(
        (x[0], sort_indices([y[1] for y in x[1]])) for x in groupby(sorted(index_sets), lambda x: x[0])
    )


class GraylogElasticsearch:
    def __init__(self, es, max_indices, backup_dir):
        self.es = es
        self.max_indices = max_indices
        self.backup_dir = backup_dir

    def indices(self):
        return list(self.es.indices.get_mapping().keys())

    def indices_to_archive(self):
        indices_sorted = group_and_sort_indices(self.indices())
        to_be_archieved = [idx[self.max_indices:] for idx in indices_sorted.values()]
        return list(chain(*to_be_archieved)) # keeps the max indices from each index set

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

        shutil.rmtree(location, ignore_errors=True)
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
