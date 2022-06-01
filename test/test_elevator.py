import unittest

from src_imports import Elevator
from src_imports import constants


class TestElevator(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.elevators = []
        for i in range(10):
            self.elevators.append(Elevator(id=i, capacity=i, cur_floor=i, steps_per_stop=i))
        return

    def test_unique_memory(self):
        for i in range(len(self.elevators)):
            # Check that parameters are set correctly for each elevator
            self.assertEqual(i, self.elevators[i].id)
            self.assertEqual(i, self.elevators[i].capacity)
            self.assertEqual(i, self.elevators[i].cur_floor)
            self.assertEqual(i, self.elevators[i].steps_per_stop)

            # Check that people_by_destination is unique for each elevator (adding a key in one won't add it to another)
            self.elevators[i].people_by_destination["test"] = 0
            self.assertFalse("test" in self.elevators[i-1].people_by_destination.keys())
            self.elevators[i].people_by_destination.pop("test") # Revert for next iteration

            # Check that up_stops, down_stops, steps_idle, and steps_active are unique for each elevator
            self.elevators[i].up_stops.append(0)
            self.elevators[i].down_stops.append(0)
            self.elevators[i].steps_idle[0] += 1
            self.elevators[i].steps_active[0] += 1

            self.assertNotEqual(len(self.elevators[i].up_stops), len(self.elevators[i-1].up_stops))
            self.assertNotEqual(len(self.elevators[i].down_stops), len(self.elevators[i-1].down_stops))
            self.assertNotEqual(self.elevators[i].steps_idle[0], self.elevators[i-1].steps_idle[0])
            self.assertNotEqual(self.elevators[i].steps_active[0], self.elevators[i-1].steps_active[0])

            # Revert for next iteration
            self.elevators[i].up_stops.pop(0)
            self.elevators[i].down_stops.pop(0)
            self.elevators[i].steps_idle[0] -= 1
            self.elevators[i].steps_active[0] -= 1
