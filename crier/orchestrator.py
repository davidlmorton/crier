from crier.script import Script


class Orchestrator:
    def __init__(self):
        self.scripts = []
        self.active_script_idx = 0

    def set_scripts(self, scripts_data):
        for script_data in scripts_data:
            self.scripts.append(Script(**script_data))
        self.active_script_idx = 0

    @property
    def active_script(self):
        return self.scripts[self.active_script_idx]

    def next_response(self):
        if not self.is_done:
            result = self.active_script.next_response()
            if self.active_script.is_done:
                self.active_script_idx += 1
            return result
        else:
            raise RuntimeError("No more scripts")

    @property
    def is_done(self):
        return self.active_script_idx >= len(self.scripts)
