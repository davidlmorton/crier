import unittest
from crier.script_master import ScriptMaster


class MockScript:
    def __init__(self, repeat=0):
        self.repeat = repeat


class TestScriptMaster(unittest.TestCase):
    def test_single(self):
        sm = ScriptMaster()

        self.assertTrue(sm.is_done)

        s1 = MockScript()

        sm.set_scripts([s1])
        self.assertFalse(sm.is_done)
        sm.advance()
        self.assertTrue(sm.is_done)
        with self.assertRaises(RuntimeError):
            sm.advance()

    def test_double(self):
        sm = ScriptMaster()

        s1 = MockScript()
        s2 = MockScript()

        sm.set_scripts([s1, s2])
        self.assertIs(s1, sm.current_script)
        sm.advance()
        self.assertIs(s2, sm.current_script)
        sm.advance()
        self.assertIs(None, sm.current_script)

    def test_multiple_with_repeats(self):
        sm = ScriptMaster()

        s1 = MockScript()
        s2 = MockScript()
        s3 = MockScript(repeat=1)

        sm.set_scripts([s1, s2, s3])
        self.assertIs(s1, sm.current_script)
        sm.advance()
        self.assertIs(s2, sm.current_script)
        sm.advance()
        self.assertIs(s3, sm.current_script)
        sm.advance()
        self.assertIs(s3, sm.current_script)
        sm.advance()
        self.assertIs(None, sm.current_script)

    def test_repeat_forever(self):
        sm = ScriptMaster()

        s1 = MockScript(repeat=-1)

        sm.set_scripts([s1])
        for i in range(9):
            self.assertIs(s1, sm.current_script)
            sm.advance()
