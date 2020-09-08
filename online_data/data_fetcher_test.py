import unittest
from online_data.data_fetcher import DataFetcher
from nose.tools import assert_equal, assert_true, assert_false, raises
from online_data.api_get_operations import operations, URL, FREQUENCY


class DataFetcherTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @staticmethod
    def test_constructor_of_class():
        f = DataFetcher('some_dir', 'key')
        assert_equal(len(f.records), 0)

    def test_add_record_returns_true(self):
        f = DataFetcher('some_dir', 'key')
        assert_true(f.is_record_updated('A'))

    def test_record_update_add_same_record_returns_false(self):
        f = DataFetcher('some_dir', 'key')
        operations.update({'A': {URL: 'a', FREQUENCY: 2}})
        assert_true(f.is_record_updated('A'))
        assert_false(f.is_record_updated('A'))
