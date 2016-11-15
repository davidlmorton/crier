import json
import subprocess
import time

__all__ = ['Webserver']


class Webserver:
    def __init__(self, response_codes, timeout=25):
        self.response_codes = response_codes
        self.timeout = timeout

        self._webserver = None

    def start(self):
        if self._webserver:
            return
        command_line = ['crier',
                        '--stop-after', str(self.timeout),
                        '--response-codes']
        command_line.extend(map(str, self.response_codes))
        self._webserver = subprocess.Popen(
            command_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self._wait()
        self._port = int(self._webserver.stderr.readline().rstrip())

    def stop(self):
        while self._webserver is not None:
            exit_code = self._webserver.poll()
            if exit_code is not None:
                if exit_code == 0:
                    stdout, stderr = self._webserver.communicate()
                    self._webserver = None
                    self._webserver_stdout = stdout
                    self._webserver_stderr = stderr

                    return map(json.loads, stdout.split('\n')[:-1])
                elif exit_code == -14:
                    raise RuntimeError(
                            "Webserver timed out after (%s) seconds" %
                            self.timeout)
                else:
                    raise RuntimeError("Webserver exited non-zero (%s)" %
                            exit_code)
            else:
                self._wait()

    def _wait(self):
        time.sleep(1)

    @property
    def url(self):
        return 'http://localhost:%d/' % self._port
