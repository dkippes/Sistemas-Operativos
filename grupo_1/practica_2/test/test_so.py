import unittest

from hardware import ASM
from so import Program, Kernel


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

    def test_kernel_ready_queue(self):
        prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.EXIT(1)])
        kernel = Kernel
        kernel.ready_queue = [prg1]
        self.assertEqual(kernel.ready_queue, [prg1])


if __name__ == '__main__':
    unittest.main()
