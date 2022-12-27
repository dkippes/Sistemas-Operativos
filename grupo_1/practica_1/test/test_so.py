import unittest

from hardware import ASM
from so import Program


class OperativeSystemTest(unittest.TestCase):
    def test_instruction_in_the_program(self):
        prg = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.EXIT(1)])
        current_instructions = prg.instructions
        expected_instructions = ['CPU', 'CPU', 'IO', 'CPU', 'CPU', 'CPU', 'EXIT']
        self.assertEqual(current_instructions, expected_instructions)

    def test_instruction_when_there_is_none_exit(self):
        prg = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3)])
        current_instructions = prg.instructions
        expected_instructions = ['CPU', 'CPU', 'IO', 'CPU', 'CPU', 'CPU', 'EXIT']
        self.assertEqual(current_instructions, expected_instructions)


if __name__ == '__main__':
    unittest.main()
