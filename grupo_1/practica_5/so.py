#!/usr/bin/env python
from enum import Enum

from hardware import *
import log


## emulates a compiled program
class Program:

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


class FirstComeFirstServeDequeueCriteria:

    def dequeue(self, queue):
        return queue.pop(0)

    def last(self, queue):
        return queue[len(queue) - 1]


class MaximumPriorityDequeueCriteria:

    def dequeue(self, queue):
        # Return a process with the maximum priority from the enqueue
        # Lower is the priority number in a process, higher is the priority itself
        # Fails if the provided enqueue is empty
        queue.sort(key=lambda process: process.priority)
        return queue.pop(0)

    def last(self, queue):
        queue.sort(key=lambda process: process.priority)
        return queue[len(queue) - 1]


class ReadyQueue:

    def __init__(self, dequeue_criteria=FirstComeFirstServeDequeueCriteria()):
        self._queue = []
        self._dequeue_criteria = dequeue_criteria

    def is_empty(self):
        return len(self._queue) == 0

    def enqueue(self, process):
        self._queue.append(process)

    def dequeue(self):
        return self._dequeue_criteria.dequeue(self._queue)

    def last(self):
        return self._dequeue_criteria.last(self._queue)

    @property
    def queue(self):
        return self._queue


class Scheduler():

    def __init__(self):
        self._ready_queue = None

    def ready_queue(self):
        # The subclasses must implement this method
        pass

    def add(self, process):
        self.ready_queue().enqueue(process)

    def get_next(self):
        return self.ready_queue().dequeue()

    def must_expropriate(self, pcb, other_pcb):
        return False

    def can_add(self):
        return not self.ready_queue().is_empty()


class FirstComeFirstServeScheduler(Scheduler):

    def ready_queue(self):
        # I use lazy initialization because I have no idea how can I make this the other way
        if self._ready_queue is None:
            self._ready_queue = ReadyQueue()
        return self._ready_queue


class PriorityScheduler(Scheduler):

    def __init__(self):
        super().__init__()
        HARDWARE.clock.addSubscriber(self)
        self._current_clock = 5

    def ready_queue(self):
        if self._ready_queue is None:
            self._ready_queue = ReadyQueue(MaximumPriorityDequeueCriteria())
        return self._ready_queue

    def tick(self, number):
        if number >= self._current_clock:
            self._current_clock += 5
            if not self.ready_queue().is_empty():
                last = self.ready_queue().last()
                last.priority = max(0, last.priority - 1)


class PreemptivePriorityScheduler(PriorityScheduler):

    def must_expropriate(self, running_pcb, pcb):
        return running_pcb.priority > pcb.priority


class RoundRobinScheduler(Scheduler):

    def __init__(self, quantum):
        super().__init__()
        HARDWARE.timer.quantum = quantum

    def ready_queue(self):
        # I use lazy initialization because I have no idea how can I make this the other way
        if self._ready_queue is None:
            self._ready_queue = ReadyQueue()
        return self._ready_queue


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


class TimeOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        running_pcb = self.kernel.pcb_table.running_pcb
        self.kernel.dispatcher.save(running_pcb)
        self.kernel.scheduler.add(running_pcb)
        running_pcb.set_as(STATE.READY)

        next_to_run = self.kernel.scheduler.get_next()
        self.kernel.pcb_table.running_pcb = next_to_run
        self.kernel.dispatcher.load(next_to_run)


class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb = self.kernel.pcb_table.running_pcb
        pcb.set_as(STATE.TERMINATED)
        self.kernel.dispatcher.save(pcb)
        self.kernel.pcb_table.remove_running_pcb()
        frames_to_be_free = list(pcb.page_table.values())
        self.kernel.memory_manager.release_frames(frames_to_be_free)

        if self.kernel.scheduler.can_add():
            pcb_to_load = self.kernel.scheduler.get_next()
            self.kernel.pcb_table.running_pcb = pcb_to_load
            self.kernel.dispatcher.load(pcb_to_load)


class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        program_name = irq.parameters[0]
        priority = irq.parameters[1]
        pid = self.kernel.pcb_table.get_new_pid()
        pcb = PCB(program_name, priority, pid)
        self.kernel.loader.load(pcb)
        self.kernel.pcb_table.add(pcb)

        if self.kernel.pcb_table.has_a_process_running():
            running = self.kernel.pcb_table.running_pcb
            if self.kernel.scheduler.must_expropriate(running, pcb):
                self.kernel.dispatcher.save(running)
                self.kernel.scheduler.add(running)
                running.set_as(STATE.READY)
                self.kernel.pcb_table.running_pcb = pcb
                self.kernel.dispatcher.load(pcb)
            else:
                pcb.set_as(STATE.READY)
                self.kernel.scheduler.add(pcb)
        else:
            self.kernel.pcb_table.running_pcb = pcb
            self.kernel.dispatcher.load(pcb)


class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        instruction = irq.parameters[0]
        pcb_running = self.kernel.pcb_table.running_pcb
        pcb_running.set_as(STATE.WAITING)
        self.kernel.pcb_table.remove_running_pcb()
        self.kernel.dispatcher.save(pcb_running)
        self.kernel.ioDeviceController.runOperation(pcb_running, instruction)

        if self.kernel.scheduler.can_add():
            pcb_to_load = self.kernel.scheduler.get_next()
            self.kernel.dispatcher.load(pcb_to_load)
            self.kernel.pcb_table.running_pcb = pcb_to_load

        log.logger.info(self.kernel.ioDeviceController)


class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb = self.kernel.ioDeviceController.getFinishedPCB()

        if self.kernel.pcb_table.running_pcb:
            running = self.kernel.pcb_table.running_pcb
            if self.kernel.scheduler.must_expropriate(running, pcb):
                self.kernel.dispatcher.save(running)
                self.kernel.scheduler.add(running)
                running.set_as(STATE.READY)
                self.kernel.pcb_table.running_pcb = pcb
                self.kernel.dispatcher.load(pcb)
            else:
                pcb.set_as(STATE.READY)
                self.kernel.scheduler.add(pcb)
        else:
            self.kernel.dispatcher.load(pcb)
            self.kernel.pcb_table.running_pcb = pcb

        log.logger.info(self.kernel.ioDeviceController)


class FileSystem:

    def __init__(self):
        self._files = dict()

    def write(self, path, instructions):
        self._files[path] = instructions

    def read(self, path):
        return self._files[path]


# emulates the core of an Operative System
class Kernel:

    def __init__(self, scheduler, frame_size):
        HARDWARE.mmu.frameSize = frame_size
        ## setup interruption handlers
        newHandler = NewInterruptionHandler(self)
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, newHandler)

        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)

        timeOutHandler = TimeOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(TIMEOUT_INTERRUPTION_TYPE, timeOutHandler)

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        self._dispatcher = Dispatcher()
        self._file_system = FileSystem()
        self._memory_manager = MemoryManager()
        self._loader = Loader(self._file_system, self._memory_manager)
        self._pcb_table = PCBTable()
        self._scheduler = scheduler

    @property
    def file_system(self):
        return self._file_system

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
    def scheduler(self):
        return self._scheduler

    @property
    def memory_manager(self):
        return self._memory_manager

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    ## emulates a "system call" for programs execution
    def run(self, path, priority):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, [path, priority])
        HARDWARE.interruptVector.handle(newIRQ)
        log.logger.info("\n Executing program: {name}".format(name=path))
        log.logger.info(HARDWARE)

    def __repr__(self):
        return "Kernel "


class PCB:
    def __init__(self, path, priority, pid):
        self._pid = pid
        self._path = path
        self._pc = 0
        self._priority = priority
        self._state = STATE.NEW
        self._page_table = dict()

    @property
    def page_table(self):
        return self._page_table

    def set_page_table(self, page_id, frame_id):
        self._page_table[page_id] = frame_id

    @property
    def path(self):
        return self._path

    def set_as(self, state):
        self._state = state

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        # I allow the change of the priority during the object's life to avoid starvation
        self._priority = priority

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

class MemoryManager:

    def __init__(self):
        size = HARDWARE.memory.size // HARDWARE.mmu.frameSize
        self._free_frames = list(range(0, size))
        self._allocated_frames = []

    def allocate_frames(self, frame_limit):
        frames_to_allocate = self._free_frames[0:frame_limit]
        for frame in frames_to_allocate:
            self._free_frames.remove(frame)
            self._allocated_frames.append(frame)
        return frames_to_allocate

    def release_frames(self, frames_to_be_released):
        for frame in frames_to_be_released:
            self._allocated_frames.remove(frame)
            self._free_frames.append(frame)



class Loader:

    def __init__(self, file_system, memory_manager):
        self._next_address = 0
        self._file_system = file_system
        self._memory_manager = memory_manager

    def split(self, list, length):
        return [list[i:i + length] for i in range(0, len(list), length)]

    def load(self, pcb):
        path = pcb.path
        instructions = self._file_system.read(path).instructions
        frame_length = HARDWARE.mmu.frameSize
        result = len(instructions) // frame_length
        remainder = len(instructions) % frame_length
        if remainder != 0:
            result = result + 1
        allocated_frames = self._memory_manager.allocate_frames(result)
        splitted_instructions = self.split(instructions, frame_length)
        for page_id in range(0, result):
                frame_id = allocated_frames[page_id]
                pcb.set_page_table(page_id, frame_id)
                self.write_in_memory(frame_id, splitted_instructions[page_id], frame_length)

    def write_in_memory(self, page_id, instructions_to_load, frame_length):
        for i, instruction in enumerate(instructions_to_load):
            frame_address = (page_id * frame_length) + i
            HARDWARE.memory.write(frame_address, instruction)


class Dispatcher:

    def load(self, pcb):
        HARDWARE.cpu.pc = pcb.pc
        HARDWARE.mmu.resetTLB()
        for page_id, frame_id in pcb.page_table.items():
            HARDWARE.mmu.setPageFrame(page_id, frame_id)
        HARDWARE.timer.reset()

    def save(self, pcb):
        pcb.pc = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1
