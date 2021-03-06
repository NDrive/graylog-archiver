# Graylog Archiver
Archives graylog indices to `backup_dir`, keeping the latest ones (`max_indices`).

For example, if you have the following indices:

- graylog_49
- graylog_48
- graylog_47

And `max_indices` is set to 1, it will archive and delete 48 and 47.

## Install

Install __Python 3__ and use pip:

    pip3 install graylog-archiver

## Usage
Configure `path.repo` in `elasticsearch.yml` to allow the creation of backup
repositories at `backup_dir`.


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
  "max_indices": 3,
  "backup_dir": "/srv/backups/elasticsearch/graylog",
  "delete": false
}
```

Run with:

    graylog-archiver

Use your strategy to backup:

    rsync -r --remove-source-files /srv/backups/elasticsearch/graylog backups@backups.company.com:/srv/backups/graylog

## Test
Start docker containers:

    cd test && docker-compose up -d

Setup Graylog with an input and send some logs.

Run graylog_archiver with the test configuration:

    graylog-archiver --config test/config.json
