import unittest
from online_data.api_get_operations import ApiGetWrapper
from online_data.operations_recorder import OperationsRecorder
from nose.tools import assert_equal, assert_raises, assert_is_none


class ApiGetWrapperTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @staticmethod
    def test_constructor_of_class():
        key = 'some_key'
        recorder = None
        f = ApiGetWrapper(recorder, key)
        assert_equal(f._headers['x-rapidapi-key'], key)

    @staticmethod
    def test_get_invalid_operation_returns_none():
        key = 'some_key'
        recorder = OperationsRecorder('some_dir')
        f = ApiGetWrapper(recorder, key)
        assert_is_none(f.get('InvalidOperation'))

    @staticmethod
    def test_transform_url_to_name():
        key = 'some_key'
        recorder = OperationsRecorder('some_dir')
        f = ApiGetWrapper(recorder, key)
        with assert_raises(IndexError):
            f.transform_url_to_name('no.adress.with.dat.domain/123/abc')
        assert_equal(f.transform_url_to_name(
            'www.whatever.com/123/abc/'), '123abc')
