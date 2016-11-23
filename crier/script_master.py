class ScriptMaster:
    def __init__(self):
        self.scripts = []
        self.current_script_idx = 0
        self.num_times_repeated = 0

    def set_scripts(self, scripts):
        self.scripts = scripts
        self.current_script_idx = 0
        self.num_times_repeated = 0

    @property
    def current_script(self):
        if self.is_done:
            return
        else:
            return self.scripts[self.current_script_idx]

    def advance(self):
        if self.is_done:
            raise RuntimeError("Cannot advance, already done")
        else:
            self.num_times_repeated += 1
            if (self.num_times_repeated > self.current_script.repeat and
                self.current_script.repeat != -1):
                self.num_times_repeated = 0
                self.current_script_idx += 1

        return self.is_done

    @property
    def is_done(self):
        return self.current_script_idx == len(self.scripts)
