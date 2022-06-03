import unittest

from src_imports import Building


simple_floor_populations = [1, 1] # Two floor building with one resident on each floor
simple_dest_floors_by_state_name = {
    "freetime": [1,2], # Person can go anywhere during freetime
    "class": [1], # Must go to ground floor for in person class
    "sleep": [], # Sleep only happens at person's home floor
    "meal": [1], # Must go to ground floor to eat out / pickup food
    "exercise": [1], # Send to ground floor
    "shop": [1], # Must go to ground floor to go to store
    "chores": [], # Chores only happen at person's home floor
    "study": [1], # Send to ground floor
}
simple_elevator_starting_floors = [0, 1] # Two elevators, one starting on 1st and other starting on 2nd floors
simple_elevator_capacity = 10
simple_elevator_algorithm = "stay_where_stopped"
simple_elevator_steps_per_stop = 5 # Num simulation steps an elevator must pass (doing nothing) each time it stops to onload or offload passengers


class TestBuilding(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        return
    
    def test_unique_memory(self):
        building = Building(simple_floor_populations, simple_dest_floors_by_state_name, simple_elevator_starting_floors, simple_elevator_capacity, simple_elevator_algorithm, simple_elevator_steps_per_stop)

        # Ensure all the parameter data trickled down to sub-classes properly
        self.assertEqual(len(simple_floor_populations), len(building.floors))
        self.assertEqual(simple_floor_populations[0], len(building.floors[0].people_on_floor))
        self.assertEqual(simple_floor_populations[1], len(building.floors[1].people_on_floor))

        self.assertEqual(len(simple_elevator_starting_floors), len(building.elevators))
        self.assertEqual(simple_elevator_starting_floors[0], building.elevators[0].cur_floor)
        self.assertEqual(simple_elevator_starting_floors[1], building.elevators[1].cur_floor)

        self.assertEqual(simple_elevator_capacity, building.elevators[0].capacity)
        self.assertEqual(simple_elevator_capacity, building.elevators[1].capacity)

        self.assertEqual(simple_elevator_algorithm, building.elevator_algorithm.algorithm)

        self.assertEqual(simple_elevator_steps_per_stop, building.elevators[0].steps_per_stop)
        self.assertEqual(simple_elevator_steps_per_stop, building.elevators[1].steps_per_stop)

        # Ensure that each floor and elevator have unique memory
        self.assertNotEqual(building.floors[0].id, building.floors[1].id)
        self.assertNotEqual(building.floors[0].people_on_floor, building.floors[1].people_on_floor)

        self.assertNotEqual(building.elevators[0].id, building.elevators[1].id)
        self.assertNotEqual(building.elevators[0].cur_floor, building.elevators[1].cur_floor)

        # Increment active counter of one elevator and idle counter of the other and ensure they don't interfere
        test_day = 0
        building.elevators[0].steps_active[0] += 1
        building.elevators[1].steps_idle[0] += 1
        self.assertEqual(1, building.elevators[0].steps_active[test_day])
        self.assertEqual(0, building.elevators[0].steps_idle[test_day])
        self.assertEqual(1, building.elevators[1].steps_idle[test_day])
        self.assertEqual(0, building.elevators[1].steps_active[test_day])
        return
    
    def test_generate_floors(self):
        return
    
    def test_generate_elevators(self):
        return

"""
The Building class depends on the Elevator, Floor, and Person classes
"""