import unittest

from src_imports import Simulation
from src_imports import Building
from src_imports import Person

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
simple_elevator_starting_floors = [1, 1] # Two elevators, both starting at ground floor
simple_elevator_capacity = 10
simple_elevator_algorithm = "stay_where_stopped"
simple_elevator_steps_per_stop = 5 # Num simulation steps an elevator must pass (doing nothing) each time it stops to onload or offload passengers

class TestSimulation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Runs once before all tests
        return
    
    def setUp(self):
        # Runs before each test
        self.building = Building(simple_floor_populations, simple_dest_floors_by_state_name, simple_elevator_starting_floors, simple_elevator_capacity, simple_elevator_algorithm, simple_elevator_steps_per_stop)


    def test_state_change_travel_down(self):
        return

    def test_state_change_travel_up(self):
        return
        
    def test_handle_state_change(self):
        day = 0
        home_floor_id = 2
        person = self.building.floors[home_floor_id].people_on_floor[0] # Only person on second floor
        person.state_change_ids[day][0] = (2, 1) # Set first state change to change from sleep to class
        person.dest_floors_by_state_name["class"] = [1] # Ensure that the only dest floor for class for this person is floor 1
        
        # Ensure the test data we just set is properly reflected within the Building
        self.assertEqual(2, self.building.floors[home_floor_id-1].people_on_floor[0].state_change_ids[day][0, 0])
        self.assertEqual(1, self.building.floors[home_floor_id-1].people_on_floor[0].state_change_ids[day][0, 1])
        self.assertEqual([1], self.building.floors[home_floor_id-1].people_on_floor[0].dest_floors_by_state_name["class"])

        Simulation.handle_state_change(self.building, day, person) # The function we are testing
        # What should happen: Person needs to travel down to first floor. Person should be removed from people_on_floor and added to people_going_down on the same floor.
        # This is the first person to be added to people_going_down, so the floor's is_down_pressed should be updated and the floor id should be added to the building's floors_new_down_button.
        self.assertEqual([], self.building.floors[home_floor_id-1].people_on_floor)
        self.assertEqual(1, len(self.building.floors[home_floor_id-1].people_going_down))
        self.assertEqual(person, self.building.floors[home_floor_id-1].people_going_down[0])
        self.assertEqual(True, self.building.floors[home_floor_id-1].is_down_pressed)
        self.assertEqual(home_floor_id, self.building.floors_new_down_button[0])
        
        return 

    # Covered by test above
    def test_handle_state_changes(self):
        return

    def test_update_counters(self):
        return
    
    def test_handle_new_button_presses(self):
        return

    def test_update_active_elevators(self):
        return

    def test_update_idle_elevators(self):
        return
    
    # Covered by two tests above
    def update_elevators(self):
        return 