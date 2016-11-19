class Script:
    def __init__(self, status_code, headers=None, response=None, repeat=0):
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.response = response if response is not None else {}
        self.repeat = repeat
        self.count = 0

    def next_response(self):
        if not self.is_done:
            self.count += 1
            return self.response, self.status_code, self.headers
        else:
            raise RuntimeError("Script repeated too many times")

    @property
    def is_done(self):
        if self.repeat == -1:
            return False
        else:
            return self.count > self.repeat
