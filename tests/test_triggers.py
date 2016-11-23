from crier import Webserver
from crier.script import Script
import requests
import unittest


class TestTriggers(unittest.TestCase):
    def test_two_webservers_chatting(self):
        last_script = Script(status_code=200)
        a_scripts = make_scripts(25251) + [last_script]
        b_scripts = make_scripts(25250)
        a = Webserver(port=25250, scripts=a_scripts, timeout=5)
        b = Webserver(port=25251, scripts=b_scripts, timeout=5)

        a.start()
        b.start()

        response = requests.post(a.url, {})

        self.assertEqual(200, response.status_code)

        a_records = a.stop()
        b_records = b.stop()

        self.assertEqual(3, len(a_records))
        self.assertEqual(2, len(b_records))


def make_scripts(port):
    return [
        Script(status_code=200,
               after_response={'method': 'POST',
                               'url': 'http://localhost:%s/' % port,
                               'body': {}},
               repeat=1),
    ]
