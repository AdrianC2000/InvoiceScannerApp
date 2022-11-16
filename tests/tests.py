import unittest

from settings.settings import customize_json, change_keys


class TestSum(unittest.TestCase):

    def test_null_if_no_nulls(self):
        self.assertEqual({"a": "b"}, customize_json({'a': 'b'}), "Error")

    def test_null_if_single_null(self):
        self.assertEqual({"a": "b"}, customize_json({'a': 'b', 'c': None}), "Error")

    def test_null_if_nested_null(self):
        self.assertEqual({"a": "b", 'array': [{'d': 'b'}]},
                         customize_json({'a': 'b', 'array': [{'c': None}, {'d': 'b'}]}), "Error")

    def test_key_not_changed(self):
        self.assertEqual({'a': 'b'}, change_keys({'a': 'b'}, 'b', 'c', False), "Error")

    def test_key_simple_changed(self):
        self.assertEqual({'c': 'b'}, change_keys({'a': 'b'}, 'a', 'c', False), "Error")

    def test_key_nested_changed(self):
        self.assertEqual({'a': 'b', 'array': [{'c': None}, {'abc': 'b'}]},
                         change_keys({'a': 'b', 'array': [{'c': None}, {'d': 'b'}]}, 'd', 'abc', False),
                         "Error")

    def test_key_deleted(self):
        self.assertEqual({'a': 'b'}, change_keys({'a': 'b'}, 'b', 'c', True), "Error")

    def test_key_simple_deleted(self):
        self.assertEqual({}, change_keys({'a': 'b'}, 'a', 'c', True), "Error")

    def test_key_nested_deleted(self):
        self.assertEqual({'a': 'b', 'array': [{'c': None}]},
                         change_keys({'a': 'b', 'array': [{'c': None}, {'d': 'b'}]}, 'd', 'abc', True),
                         "Error")


if __name__ == '__main__':
    unittest.main()
