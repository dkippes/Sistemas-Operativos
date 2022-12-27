#!/usr/bin/env python
from enum import Enum

from hardware import *
import log


## emulates a compiled program
class Program():

    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addInstr(self, instruction):
        self._instructions.append(instruction)

    def expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                ## is a list of instructions
                expanded.extend(i)
            else:
                ## a single instr (a String)
                expanded.append(i)

        ## now test if last instruction is EXIT
        ## if not... add an EXIT as final instruction
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


## emulates an Input/Output device controller (driver)
class IoDeviceController():

    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPCB = None

    def runOperation(self, pcb, instruction):
        pair = {'pcb': pcb, 'instruction': instruction}
        # append: adds the element at the end of the queue
        self._waiting_queue.append(pair)
        # try to send the instruction to hardware's device (if is idle)
        self.__load_from_waiting_queue_if_apply()

    def getFinishedPCB(self):
        finishedPCB = self._currentPCB
        self._currentPCB = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPCB

    def __load_from_waiting_queue_if_apply(self):
        if (len(self._waiting_queue) > 0) and self._device.is_idle:
            ## pop(): extracts (deletes and return) the first element in queue
            pair = self._waiting_queue.pop(0)
            # print(pair)
            pcb = pair['pcb']
            instruction = pair['instruction']
            self._currentPCB = pcb
            self._device.execute(instruction)

    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}".format(
            deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)


## emulates the  Interruptions Handlers
class AbstractInterruptionHandler():

    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))


class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb = self.kernel.pcb_table.running_pcb
        pcb.set_as(STATE.TERMINATED)
        self.kernel.dispatcher.save(pcb)
        self.kernel.pcb_table.remove_running_pcb()

        if self.kernel.ready_queue:
            pcb_to_load = self.kernel.ready_queue.pop(0)
            self.kernel.pcb_table.running_pcb = pcb_to_load
            self.kernel.dispatcher.load(pcb_to_load)


class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        program = irq.parameters
        pid = self.kernel.pcb_table.get_new_pid()
        program_base_dir = self.kernel.loader.load(program)
        pcb = PCB(program_base_dir, program.name, pid)
        self.kernel.pcb_table.add(pcb)

        if self.kernel.pcb_table.has_a_process_running():
            pcb.set_as(STATE.READY)
            self.kernel.ready_queue.append(pcb)
        else:
            self.kernel.pcb_table.running_pcb = pcb
            self.kernel.dispatcher.load(pcb)


class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        instruction = irq.parameters
        pcb_running = self.kernel.pcb_table.running_pcb
        pcb_running.set_as(STATE.WAITING)
        self.kernel.pcb_table.remove_running_pcb()
        self.kernel.dispatcher.save(pcb_running)
        self.kernel.ioDeviceController.runOperation(pcb_running, instruction)

        if self.kernel.ready_queue:
            pcb_to_load = self.kernel.ready_queue.pop(0)
            self.kernel.dispatcher.load(pcb_to_load)
            self.kernel.pcb_table.running_pcb = pcb_to_load

        log.logger.info(self.kernel.ioDeviceController)


class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb = self.kernel.ioDeviceController.getFinishedPCB()

        if self.kernel.pcb_table.running_pcb:
            pcb.set_as(STATE.READY)
            self.kernel.ready_queue.append(pcb)
        else:
            self.kernel.dispatcher.load(pcb)
            self.kernel.pcb_table.running_pcb = pcb

        log.logger.info(self.kernel.ioDeviceController)


# emulates the core of an Operative System
class Kernel:

    def __init__(self):
        ## setup interruption handlers
        newHandler = NewInterruptionHandler(self)
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, newHandler)

        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        self._dispatcher = Dispatcher()
        self._loader = Loader()
        self._pcb_table = PCBTable()
        self._ready_queue = []

    @property
    def dispatcher(self):
        return self._dispatcher

    @property
    def loader(self):
        return self._loader

    @property
    def pcb_table(self):
        return self._pcb_table

    @property
    def ready_queue(self):
        return self._ready_queue

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    ## emulates a "system call" for programs execution
    def run(self, program):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, program)
        HARDWARE.interruptVector.handle(newIRQ)
        log.logger.info("\n Executing program: {name}".format(name=program.name))
        log.logger.info(HARDWARE)

    def __repr__(self):
        return "Kernel "


class PCB:
    def __init__(self, base_dir, path, pid):
        self._pid = pid
        self._base_dir = base_dir
        self._path = path
        self._pc = 0
        self._state = STATE.NEW

    def set_as(self, state):
        self._state = state

    @property
    def base_dir(self):
        return self._base_dir

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, pc):
        self._pc = pc

    def __repr__(self):
        return "PCB({pid}, {state})".format(pid=self._pid, state=self._state)

class STATE(Enum):
    NEW = "new"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    TERMINATED = "terminated"


class PCBTable:

    def __init__(self):
        self._table = []
        self._running_pcb = None

    def get_new_pid(self):
        return len(self._table)

    def get(self, pid):
        return self._table[pid]

    def add(self, pcb):
        self._table.append(pcb)

    def remove(self, pid):
        self._table.remove(self.get(pid))

    def has_a_process_running(self):
        return self._running_pcb is not None

    def remove_running_pcb(self):
        self._running_pcb = None

    @property
    def running_pcb(self):
        return self._running_pcb

    @running_pcb.setter
    def running_pcb(self, pcb):
        pcb.set_as(STATE.RUNNING)
        self._running_pcb = pcb


class Loader:

    def __init__(self):
        self._next_address = 0

    def load(self, program):
        # loads the program in main memory
        program_size = len(program.instructions)
        for index in range(self._next_address, program_size + self._next_address):
            inst = program.instructions[index - self._next_address]
            HARDWARE.memory.write(index, inst)
        base_dir = self._next_address
        self._next_address += program_size
        return base_dir


class Dispatcher:

    def load(self, pcb):
        HARDWARE.cpu.pc = pcb.pc
        HARDWARE.mmu.baseDir = pcb.base_dir

    def save(self, pcb):
        pcb.pc = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1