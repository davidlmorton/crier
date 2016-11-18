from crier.validator import load_and_validate
import json
import unittest


class TestWebserver(unittest.TestCase):
    def test_passes_validation(self):
        expected_data = [{'status_code': 200}]
        data_str = json.dumps(expected_data)
        self.assertEqual(expected_data, load_and_validate(data_str))

    def test_status_code_not_integer(self):
        data = [{'status_code': 'foo'}]
        data_str = json.dumps(data)
        with self.assertRaises(Exception):
            load_and_validate(data_str)
