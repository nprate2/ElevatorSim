import unittest
import numpy as np
from tqdm import tqdm

from src_imports import Floor

test_dest_floors_by_state_name = {
    "freetime": [],
    "class": [],
    "sleep": [],
    "meal": [],
    "exercise": [],
    "shop": [],
    "chores": [],
    "study": [],
}

class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #print("-----TESTING PERSON-----")
        self.floors = []
        for i in range(10): # Produces floors with ids 0-9 (10 floors)
            floor = Floor(id=i, num_residents=i+1, building_dest_floors_by_state_name=test_dest_floors_by_state_name)
            self.floors.append(floor)
        return

    def test_unique_memory(self):
        # Ensure id, num_residents, and people_on_floor generate correctly for each floor
        for i in range(len(self.floors)):
            self.assertEqual(i, self.floors[i].id)
            self.assertEqual(i+1, self.floors[i].num_residents)
            self.assertEqual(i+1, len(self.floors[i].people_on_floor))

            # Ensure updating people_going_up on one floor didn't update it for other floors
            person = self.floors[i].people_on_floor[0]
            self.floors[i].people_on_floor.pop(0)
            self.floors[i].people_going_up.append(person)

            self.assertNotEqual(len(self.floors[i].people_going_up), len(self.floors[i-1].people_going_up))
            # Revert to original state for next iteration
            self.floors[i].people_on_floor.append(person)
            self.floors[i].people_going_up.pop(0)

            # Ensure updating people_going_down on one floor didn't update it for other floors
            person = self.floors[i].people_on_floor[0]
            self.floors[i].people_on_floor.pop(0)
            self.floors[i].people_going_down.append(person)
            
            self.assertNotEqual(len(self.floors[i].people_going_down), len(self.floors[i-1].people_going_down))
            # Revert to original state for next iteration
            self.floors[i].people_on_floor.append(person)
            self.floors[i].people_going_down.pop(0)
