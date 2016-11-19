import unittest
from crier.orchestrator import Orchestrator


class TestOrchestrator(unittest.TestCase):
    def test_normal_operation(self):
        o = Orchestrator()

        self.assertTrue(o.is_done)

        status_code = 123
        headers = {'foo': 'bar'}
        response = {'baz': 'qux'}
        scripts_data = [{
            'status_code': status_code,
            'headers': headers,
            'response': response,
            'repeat': 1,
        }]
        o.set_scripts(scripts_data)

        expected_response = (response, status_code, headers)
        self.assertFalse(o.is_done)
        self.assertEqual(expected_response, o.next_response())

        self.assertFalse(o.is_done)
        self.assertEqual(expected_response, o.next_response())

        self.assertTrue(o.is_done)
        with self.assertRaises(RuntimeError):
            o.next_response()
