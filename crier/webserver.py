from crier.script import Script

import json
import yaml
import subprocess
import time

__all__ = ['Webserver']


class Webserver:
    def __init__(self, scripts, port=None, timeout=25):
        self.port = port
        self.scripts = scripts
        self.timeout = timeout

        self._webserver = None
        self._webserver_stdout = None
        self._webserver_stderr = None

    @property
    def scripts_string(self):
        pure_data = []
        for script in self.scripts:
            if isinstance(script, Script):
                pure_data.append(script.as_dict)
            else:
                pure_data.append(script)
        return pure_data

    def start(self):
        if self._webserver:
            return
        command_line = ['crier',
                        '--timeout', str(self.timeout),
                        '--scripts']
        command_line.append(json.dumps(self.scripts_string))

        if self.port is not None:
            command_line.extend(['--port', str(self.port)])

        self._webserver = subprocess.Popen(
            command_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self._wait()
        line = self._webserver.stderr.readline().rstrip()

        try:
            self._port = int(line)
        except:
            # this ensures that the reason the crier subprocess didn't start is
            # printed before the exception traceback.
            print line
            for line in self._webserver.stderr.readlines():
                print line.rstrip()
            raise

    @property
    def history(self):
        if self._webserver_stdout is None:
            return []
        else:
            return yaml.load(self._webserver_stdout)

    def stop(self):
        while self._webserver is not None:
            exit_code = self._webserver.poll()
            if exit_code is not None:
                if exit_code == 0:
                    stdout, stderr = self._webserver.communicate()
                    self._webserver = None
                    self._webserver_stdout = stdout
                    self._webserver_stderr = stderr

                    return self.history
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
