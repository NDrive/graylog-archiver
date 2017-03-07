import argparse

from elasticsearch import Elasticsearch

from .archiver import Archiver
from .config import Config
from .logs import configure_logs


def to_elasticsearch(hosts):
    return Elasticsearch(hosts.split(","))


def parse():
    parser = argparse.ArgumentParser(
        description="Archives Graylog closed indices with rsync."
    )

    parser.add_argument(
        '--file', '-f',
        help='JSON Configuration file',
        default="graylog_archiver.json"
    )

    args = parser.parse_args()
    return args


def main():
    args = parse()
    configure_logs()
    config = Config(args.file)
    archiver = Archiver(config)
    archiver.archive()


if __name__ == '__main__':
    main()
