import unittest
import so


class FirstComeFirstServeSchedulerTest(unittest.TestCase):
    def test_add_and_get(self):
        scheduler = so.FirstComeFirstServeScheduler()
        pcb = so.PCB(0, 'path.exe', 8, 200)
        scheduler.add(pcb)
        self.assertTrue(scheduler.get_next(), pcb)

    def test_must_expropriate(self):
        first_pcb = so.PCB(0, 'path.exe', 8, 200)
        second_pcb = so.PCB(0, 'path.exe', 4, 201)
        self.assertFalse(so.FirstComeFirstServeScheduler().must_expropriate(first_pcb, second_pcb))


class PrioritySchedulerTest(unittest.TestCase):
    def test_add_and_get(self):
        scheduler = so.PriorityScheduler()
        first_pcb = so.PCB(0, 'path.exe', 8, 200)
        second_pcb = so.PCB(0, 'path.exe', 4, 201)
        scheduler.add(first_pcb)
        scheduler.add(second_pcb)
        self.assertTrue(scheduler.get_next(), second_pcb)
        self.assertTrue(scheduler.get_next(), first_pcb)

    def test_must_expropriate(self):
        first_pcb = so.PCB(0, 'path.exe', 8, 200)
        second_pcb = so.PCB(0, 'path.exe', 4, 201)
        self.assertFalse(so.PriorityScheduler().must_expropriate(first_pcb, second_pcb))


class PreemptivePrioritySchedulerTest(unittest.TestCase):
    def test_add_and_get(self):
        scheduler = so.PreemptivePriorityScheduler()
        first_pcb = so.PCB(0, 'path.exe', 8, 200)
        second_pcb = so.PCB(0, 'path.exe', 4, 201)
        scheduler.add(first_pcb)
        scheduler.add(second_pcb)
        self.assertTrue(scheduler.get_next(), second_pcb)
        self.assertTrue(scheduler.get_next(), first_pcb)

    def test_must_expropriate(self):
        first_pcb = so.PCB(0, 'path.exe', 8, 200)
        second_pcb = so.PCB(0, 'path.exe', 4, 201)
        self.assertTrue(so.PreemptivePriorityScheduler().must_expropriate(first_pcb, second_pcb))


class ReadyQueueTest(unittest.TestCase):
    def test_empty_queue(self):
        self.assertTrue(so.ReadyQueue().is_empty())

    def test_not_empty_after_adding_an_element(self):
        queue = so.ReadyQueue()
        queue.enqueue(so.PCB(0, 'path.exe', 1, 200))
        self.assertFalse(queue.is_empty())

    def test_dequeue_using_first_come_first_serve_criteria(self):
        first_pcb = so.PCB(0, 'path.exe', 8, 200)
        second_pcb = so.PCB(0, 'path.exe', 4, 201)
        queue = so.ReadyQueue(so.FirstComeFirstServeDequeueCriteria())
        queue.enqueue(first_pcb)
        queue.enqueue(second_pcb)
        self.assertEqual(queue.dequeue(), first_pcb)
        self.assertEqual(queue.dequeue(), second_pcb)
        self.assertTrue(queue.is_empty())

    def test_dequeue_using_maximum_priority_criteria(self):
        first_pcb = so.PCB(0, 'path.exe', 8, 200)
        second_pcb = so.PCB(0, 'path.exe', 4, 201)
        queue = so.ReadyQueue(so.MaximumPriorityDequeueCriteria())
        queue.enqueue(first_pcb)
        queue.enqueue(second_pcb)
        self.assertEqual(queue.dequeue(), second_pcb)
        self.assertEqual(queue.dequeue(), first_pcb)
        self.assertTrue(queue.is_empty())


class FirstComeFirstServeDequeueCriteriaTest(unittest.TestCase):
    def test_dequeue_over_a_single_process_queue(self):
        first_pcb = so.PCB(0, 'path.exe', 1, 200)
        criteria = so.FirstComeFirstServeDequeueCriteria()
        queue = [first_pcb]
        self.assertEqual(criteria.dequeue(queue), first_pcb)

    def test_dequeue_over_a_large_queue(self):
        first_pcb = so.PCB(0, 'path.exe', 1, 200)
        second_pcb = so.PCB(0, 'path.exe', 8, 201)
        third_pcb = so.PCB(0, 'path.exe', 4, 201)
        criteria = so.FirstComeFirstServeDequeueCriteria()
        queue = [first_pcb, second_pcb, third_pcb]
        # When i dequeue using a first come first serve dequeue criteria,
        # i expect to retrieve the oldest element in the enqueue
        self.assertEqual(criteria.dequeue(queue), first_pcb)


class MinimumPriorityDequeueCriteriaTest(unittest.TestCase):
    def test_dequeue_over_a_single_process_queue(self):
        first_pcb = so.PCB(0, 'path.exe', 1, 200)
        criteria = so.MaximumPriorityDequeueCriteria()
        queue = [first_pcb]
        self.assertEqual(criteria.dequeue(queue), first_pcb)

    def test_dequeue_over_a_large_queue(self):
        first_pcb = so.PCB(0, 'path.exe', 1, 200)
        second_pcb = so.PCB(0, 'path.exe', 8, 201)
        third_pcb = so.PCB(0, 'path.exe', 4, 202)
        criteria = so.MaximumPriorityDequeueCriteria()
        queue = [first_pcb, second_pcb, third_pcb]
        # Using the minimum priority dequeue criteria, i expect
        # to get de process with the maximum priority in the enqueue
        self.assertEqual(criteria.dequeue(queue), first_pcb)
        self.assertEqual(criteria.dequeue(queue), third_pcb)
        self.assertEqual(criteria.dequeue(queue), second_pcb)


if __name__ == '__main__':
    unittest.main()
