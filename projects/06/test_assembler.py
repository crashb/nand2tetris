import unittest
import sys


class TestAssembler(unittest.TestCase):
    # we need to re-import the module for every test in order to reset the symbol counter
    def tearDown(self):
        try:
            del sys.modules['assembler']
        except KeyError:
            pass

    def test_assemble_add(self):
        from assembler import assemble_file
        assemble_file('add/Add.asm', 'add/Add.hack')
        with open('add/Add.hack', 'r') as f:
            observed = f.readlines()
        with open('add/Add.cmp', 'r') as f:
            expected = f.readlines()
        self.assertEqual(observed, expected)

    def test_assemble_max(self):
        from assembler import assemble_file
        assemble_file('max/Max.asm', 'max/Max.hack')
        with open('max/Max.hack', 'r') as f:
            observed = f.readlines()
        with open('max/Max.cmp', 'r') as f:
            expected = f.readlines()
        self.assertEqual(observed, expected)

    def test_assemble_maxL(self):
        from assembler import assemble_file
        assemble_file('max/MaxL.asm', 'max/MaxL.hack')
        with open('max/MaxL.hack', 'r') as f:
            observed = f.readlines()
        with open('max/MaxL.cmp', 'r') as f:
            expected = f.readlines()
        self.assertEqual(observed, expected)
        
    def test_assemble_rect(self):
        from assembler import assemble_file
        assemble_file('rect/rect.asm', 'rect/rect.hack')
        with open('rect/rect.hack', 'r') as f:
            observed = f.readlines()
        with open('rect/rect.cmp', 'r') as f:
            expected = f.readlines()
        self.assertEqual(observed, expected)

    def test_assemble_rectL(self):
        from assembler import assemble_file
        assemble_file('rect/rectL.asm', 'rect/rectL.hack')
        with open('rect/rectL.hack', 'r') as f:
            observed = f.readlines()
        with open('rect/rectL.cmp', 'r') as f:
            expected = f.readlines()
        self.assertEqual(observed, expected)
        
    def test_assemble_pong(self):
        from assembler import assemble_file
        assemble_file('pong/pong.asm', 'pong/pong.hack')
        with open('pong/pong.hack', 'r') as f:
            observed = f.readlines()
        with open('pong/pong.cmp', 'r') as f:
            expected = f.readlines()
        self.assertEqual(observed, expected)

    def test_assemble_pongL(self):
        from assembler import assemble_file
        assemble_file('pong/pongL.asm', 'pong/pongL.hack')
        with open('pong/pongL.hack', 'r') as f:
            observed = f.readlines()
        with open('pong/pongL.cmp', 'r') as f:
            expected = f.readlines()
        self.assertEqual(observed, expected)


if __name__ == '__main__':
    unittest.main()
