import argparse
from elasticsearch import Elasticsearch
from graylog_archiver.graylog_archiver import GraylogArchiver
from graylog_archiver.config import Config


def parse():
    parser = argparse.ArgumentParser(
        description="Archives Graylog logs to a local directory."
    )

    parser.add_argument(
        '--config', '-c',
        help='JSON configuration file',
        type=Config,
        required=True
    )

    args = parser.parse_args()
    return args


def main():
    args = parse()

    archiver = GraylogArchiver(
        es=Elasticsearch(**args.config.get("elasticsearch")),
        max_indices=args.config.get("max_indices"),
        backup_dir=args.config.get("backup_dir"),
        delete=args.config.get("delete")
    )

    archiver.archive()


if __name__ == '__main__':
    main()
