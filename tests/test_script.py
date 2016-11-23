import unittest
from crier.script import Script


class TestScript(unittest.TestCase):
    def test_defaults(self):
        s = Script(123)

        self.assertEqual({}, s.response)
        self.assertEqual({}, s.headers)
        self.assertIs(None, s.after_response)
        self.assertEqual(0, s.repeat)

    def test_classmethod(self):
        string = '[{"status_code": 200}, {"status_code": 300}]'
        scripts = Script.from_string(string)
        self.assertEqual(2, len(scripts))
        self.assertEqual(200, scripts[0].status_code)
        self.assertEqual(300, scripts[1].status_code)
