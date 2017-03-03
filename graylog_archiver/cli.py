import argparse

from elasticsearch import Elasticsearch

from .archiver import Archiver
from .config import Config


def to_elasticsearch(hosts):
    return Elasticsearch(hosts.split(","))


def parse():
    parser = argparse.ArgumentParser(
        description="Archives Graylog closed indices with rsync."
    )

    parser.add_argument(
        '--file', '-f',
        help='YML Configuration file',
        default="graylog_archiver.yml"
    )

    args = parser.parse_args()
    return args


def main():
    args = parse()
    config = Config(args.file)
    archiver = Archiver(config)
    archiver.archive()


if __name__ == '__main__':
    main()
