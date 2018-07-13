import unittest
from graylog_archiver.graylog_elasticsearch import sort_indices, group_and_sort_indices


class TestStringMethods(unittest.TestCase):

    def test_sort_from_oldest(self):
        indices = ['graylog_9', 'graylog_36']
        indices_sorted = sort_indices(indices)
        self.assertEqual(['graylog_36', 'graylog_9'], indices_sorted)

    def test_group_and_sort_indexsets(self):
        indices = [
            'graylog_9',
            'graylog_internal_3',
            'graylog_internal_5',
            'graylog_36',
            'graylog_internal_6'
        ]
        indices_grouped = group_and_sort_indices(indices)
        self.assertEqual(['graylog_36', 'graylog_9'], indices_grouped['graylog'])
        self.assertEqual(['graylog_internal_6', 'graylog_internal_5', 'graylog_internal_3'], indices_grouped['graylog_internal'])

if __name__ == '__main__':
    unittest.main()
