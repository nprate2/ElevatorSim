import unittest
import numpy as np

from src_imports import Building

simple_floor_populations = [1, 1, 1] # Three Floors, one Person on each floor
simple_dest_floors_by_state_name = None
simple_elevator_algorithm = "return_to"
simple_elevator_starting_floors = [0, 1, 2] # Three Elevators, one starting on each Floor
simple_elevator_capacities = [5, 10, 15]
simple_elevator_steps_per_loads = [2, 4, 6] # Num simulation steps an elevator must pass (doing nothing) each time it stops to onload or offload passengers
simple_elevator_return_to_floors = [0, 1, 2]

HERE_floor_populations = [0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
HERE_dest_floors_by_state_name = None
HERE_elevator_algorithm = "stay_where_stopped"
HERE_elevator_starting_floors = [0, 0, 0]
HERE_elevator_capacities = [10, 10, 10]
HERE_elevator_steps_per_loads = [5, 5, 5] # Num simulation steps an elevator must pass (doing nothing) each time it stops to onload or offload passengers
HERE_elevator_return_to_floors = [0, 5, 10]

class TestBuilding(unittest.TestCase):
    """
    Tests that the Building() constructor produces a Building as expected.
    """
    def test_generation(self):
        simple_building = Building(simple_floor_populations, None, simple_elevator_algorithm, simple_elevator_starting_floors, simple_elevator_capacities, simple_elevator_steps_per_loads, simple_elevator_return_to_floors)
        HERE_building = Building(HERE_floor_populations, None, HERE_elevator_algorithm, HERE_elevator_starting_floors, HERE_elevator_capacities, HERE_elevator_steps_per_loads, HERE_elevator_return_to_floors)
        
        self.assertEqual(simple_elevator_algorithm, simple_building.elevator_algorithm.algorithm)
        self.assertEqual(HERE_elevator_algorithm, HERE_building.elevator_algorithm.algorithm)

        # Assert floors, elevators, floors_new_down_button, and floors_new_up_button use unique memory for each Building
        HERE_building.floors_new_up_button.append(0)
        HERE_building.floors_new_down_button.append(1)
        self.assertNotEqual(simple_building.floors, HERE_building.floors)
        self.assertNotEqual(simple_building.elevators, HERE_building.elevators)
        self.assertNotEqual(simple_building.floors_new_up_button, HERE_building.floors_new_up_button)
        self.assertNotEqual(simple_building.floors_new_down_button, HERE_building.floors_new_down_button)

        return
    
    """
    Tests that generate_floors within the Building class produces a list of Floors as expected.
    """
    def test_generate_floors(self):
        simple_building = Building(simple_floor_populations, simple_dest_floors_by_state_name, simple_elevator_algorithm, simple_elevator_starting_floors, simple_elevator_capacities, simple_elevator_steps_per_loads, simple_elevator_return_to_floors)

        # Assert the correct number of Floors were generated with the correct id, people_on_floor
        self.assertEqual(len(simple_floor_populations), len(simple_building.floors))
        for i in range(len(simple_building.floors)):
            self.assertEqual(i, simple_building.floors[i].id)
            self.assertEqual(simple_floor_populations[i], len(simple_building.floors[i].people_on_floor))
            self.assertNotEqual(simple_building.floors[i].people_on_floor, simple_building.floors[i-1].people_on_floor) # Assert different Floors use different memory for people_on_floor

        # Assert that people_on_floor, people_going_up, and people_going_down use unique memory for each Floor
        for i in range(len(simple_building.floors)):
            person_on_floor = simple_building.floors[i].people_on_floor[0]
            simple_building.floors[i].people_going_up.append(person_on_floor)
            simple_building.floors[i].people_going_down.append(person_on_floor)

        for i in range(len(simple_building.floors)):
            self.assertEqual(1, len(simple_building.floors[i].people_on_floor))
            self.assertEqual(1, len(simple_building.floors[i].people_going_up))
            self.assertEqual(1, len(simple_building.floors[i].people_going_down))

            self.assertNotEqual(simple_building.floors[i].people_on_floor, simple_building.floors[i-1].people_on_floor)
            self.assertNotEqual(simple_building.floors[i].people_going_up, simple_building.floors[i-1].people_going_up)
            self.assertNotEqual(simple_building.floors[i].people_going_down, simple_building.floors[i-1].people_going_down)

        return
    
    """
    Tests that generate_elevators within the Building class produces a list of Elevators as expected.
    """
    def test_generate_elevators(self):
        simple_building = Building(simple_floor_populations, simple_dest_floors_by_state_name, simple_elevator_algorithm, simple_elevator_starting_floors, simple_elevator_capacities, simple_elevator_steps_per_loads, simple_elevator_return_to_floors)

        # Assert the correct number of Elevators were generated with the correct id, cur_floor, capacity, and steps_per_load
        self.assertEqual(len(simple_elevator_starting_floors), len(simple_building.elevators))
        for i in range(len(simple_building.elevators)):
            self.assertEqual(i, simple_building.elevators[i].id)
            self.assertEqual(simple_elevator_starting_floors[i], simple_building.elevators[i].cur_floor)
            self.assertEqual(simple_elevator_capacities[i], simple_building.elevators[i].capacity)
            self.assertEqual(simple_elevator_steps_per_loads[i], simple_building.elevators[i].steps_per_load)

        return