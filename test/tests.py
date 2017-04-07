import unittest
from graylog_archiver.graylog_elasticsearch import sort_indices


class TestStringMethods(unittest.TestCase):

    def test_sort_from_oldest(self):
        indices = ['graylog_9', 'graylog_36']
        indices_sorted = sort_indices(indices)
        self.assertEqual(['graylog_36', 'graylog_9'], indices_sorted)


if __name__ == '__main__':
    unittest.main()
