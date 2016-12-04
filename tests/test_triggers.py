from crier import Webserver
from crier.script import Script
import requests
import unittest


class TestTriggers(unittest.TestCase):
    def test_two_webservers_chatting(self):
        a_scripts = [
                Script(status_code=200,
                   after_response='meta.responses.success'),
                Script(status_code=200)
        ]
        b_scripts = [
                Script(status_code=200,
                    after_response='meta.responses.fail'),
        ]

        a = Webserver(port=25250, scripts=a_scripts, timeout=5)
        b = Webserver(port=25251, scripts=b_scripts, timeout=5)

        a.start()
        b.start()

        to_b_from_a = {
            'meta': {
                'responses': {
                    'fail': {
                        'method': 'POST',
                        'url': 'http://localhost:%s/' % a.port,
                        'body': {},
                        'headers': {'x-foo': 'bar'},
                    },
                }
            }
        }

        to_a_from_test = {
            'meta': {
                'responses': {
                    'success': {
                        'method': 'POST',
                        'url': 'http://localhost:%s/' % b.port,
                        'body': to_b_from_a,
                        'headers': {},
                    },
                }
            }
        }

        response = requests.post(a.url, json=to_a_from_test)

        for line in a._webserver.stderr.readlines():
            print line.rstrip()
        self.assertEqual(200, response.status_code)

        a_records = a.stop()
        b_records = b.stop()

        self.assertEqual(2, len(a_records))
        self.assertEqual('bar', a_records[1]['headers']['X-Foo'])
        self.assertEqual(1, len(b_records))


def make_scripts(port):
    return [
    ]
