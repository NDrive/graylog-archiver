import shutil
from graylog_archiver import logs
from graylog_archiver.graylog_elasticsearch import GraylogElasticsearch
from graylog_archiver.utils import compress_directory


class GraylogArchiver:
    def __init__(self, es, max_indices, backup_dir, delete=False):
        self.es = es
        self.max_indices = max_indices
        self.backup_dir = backup_dir
        self.delete = delete
        self.logger = logs.create_logger()
        self.graylog = GraylogElasticsearch(es, max_indices, backup_dir)

    def archive(self):
        self.logger.info("Indices: %s" % self.graylog.indices())
        indices = self.graylog.indices_to_archive()
        self.logger.info("Archiving %s" % indices)

        for index in indices:
            self.logger.info("Archiving %s..." % index)

            self.logger.info("Dumping from elasticsearch...")
            dump_dir = self.graylog.dump(index)

            self.logger.info("Compressing directory...")
            compressed_dir = compress_directory(dump_dir)
            shutil.rmtree(dump_dir)

            if self.delete:
                self.graylog.delete_index(index)
                self.logger.info("Deleted %s" % index)
    
            self.logger.info("Archived at %s" % compressed_dir)
