# Graylog-archiver
Archives graylog indices based in their age (`graylog.max_indices`). Syncs indices backups to a remote server with rsync (`backup.remote`).


## Install

    pip install graylog-archiver

## Usage
Configure `path.repo` in `elasticsearch.yml` to allow the creation of backup
repositories (`backup.local`). This allows to save temporary indices backups to transfer them
with rsync.


Example:

```
path.repo: /srv/backups/elasticsearch
```

Create a configuration file for graylog archiver `graylog_archiver.json`:

```json
{
  "elasticsearch": {
    "hosts": "localhost"
  },
  "backup": {
    "local": "/srv/backups/elasticsearch/graylog",
    "remote": "backups@backup.server.com:/mnt/backup/graylog"
  },
  "graylog": {
    "max_indices": 3
  }
}
```

Max indices is the number of the latest indices to keep. Please make sure
your indices configuration retention in Gratlog matches this value.

Run with:

    graylog-archiver -f PATH/TO/graylog-archiver.json
