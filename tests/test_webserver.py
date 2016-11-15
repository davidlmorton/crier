from crier import Webserver
from pprint import pformat
import json
import requests
import unittest


class TestWebserver(unittest.TestCase):
    def test_timeout(self):
        server = Webserver(response_codes=[200], timeout=1)
        server.start()
        with self.assertRaises(RuntimeError):
            server.stop()

    def test_stop_before_start(self):
        server = Webserver(response_codes=[200], timeout=1)
        records = server.stop()
        self.assertEqual(None, records)

    def test_normal_exit(self):
        server = Webserver(response_codes=[202, 205], timeout=10)
        server.start()
        server.start()  # does nothing

        first_body = {'somekey': 'someval'}
        response = self.post(server.url, first_body)
        self.assertEqual(202, response.status_code)

        second_body = {'foo': 'bar'}
        response = self.post(server.url, second_body)
        self.assertEqual(205, response.status_code)

        records = server.stop()
        print "Found the following records: %s" % pformat(records)

        self.assertEqual(2, len(records))
        self.assertEqual(first_body, records[0])
        self.assertEqual(second_body, records[1])

    def post(self, url, data):
        return requests.post(url,
            headers={'content-type': 'application/json'},
            data=json.dumps(data))
