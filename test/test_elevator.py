import unittest

from src_imports import Elevator
from src_imports import constants


class TestElevator(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.elevators = []
        for i in range(10):
            self.elevators.append(Elevator(id=i, capacity=i, starting_floor=i, steps_per_load=i, return_to_floor=0))
        return

    """
    Tests that the Elevator() constructor produces an Elevator as expected.
    """
    def test_generation(self):
        for i in range(len(self.elevators)):
            # Check that parameters are set correctly for each elevator
            self.assertEqual(i, self.elevators[i].id)
            self.assertEqual(i, self.elevators[i].capacity)
            self.assertEqual(i, self.elevators[i].cur_floor)
            self.assertEqual(i, self.elevators[i].steps_per_load)

    """
    Asserts that people_by_destination, up_stops, down_stops, idle_counters, active_counters, loading_counters, and returning_counters use unique memory for each Elevator
    """
    def test_unique_memory(self):
        for i in range(len(self.elevators)):
            # Check that people_by_destination is unique for each Elevator (adding a key in one won't add it to another)
            self.elevators[i].people_by_destination[0] = 0
            self.assertFalse("test" in self.elevators[i-1].people_by_destination.keys())
            self.elevators[i].people_by_destination.pop(0) # Revert for next iteration

            # Check that up_stops, down_stops, idle_counters, active_counters, loading_counters, and returning_counters are unique for each Elevator
            self.elevators[i].up_stops.append(i)
            self.elevators[i].down_stops.append(i)
            self.elevators[i].idle_counters[0] = 1
            self.elevators[i].active_counters[0] = 1
            self.elevators[i].loading_counters[0] = 1
            self.elevators[i].returning_counters[0] = 1

            self.assertNotEqual(len(self.elevators[i].up_stops), len(self.elevators[i-1].up_stops))
            self.assertNotEqual(len(self.elevators[i].down_stops), len(self.elevators[i-1].down_stops))
            self.assertNotEqual(self.elevators[i].idle_counters[0], self.elevators[i-1].idle_counters[0])
            self.assertNotEqual(self.elevators[i].active_counters[0], self.elevators[i-1].active_counters[0])
            self.assertNotEqual(self.elevators[i].loading_counters[0], self.elevators[i-1].loading_counters[0])
            self.assertNotEqual(self.elevators[i].returning_counters[0], self.elevators[i-1].returning_counters[0])

            # Revert for next iteration
            self.elevators[i].up_stops.pop(0)
            self.elevators[i].down_stops.pop(0)
            self.elevators[i].idle_counters[0] -= 1
            self.elevators[i].active_counters[0] -= 1
            self.elevators[i].loading_counters[0] -= 1
            self.elevators[i].returning_counters[0] -= 1
