import unittest

import numpy as np

from src_imports import Simulation
from src_imports import Building
from src_imports import Person

simple_floor_populations = [1, 1] # Two floor building with one resident on each floor
simple_dest_floors_by_state_name = {
    "freetime": [0, 1], # Person can go anywhere during freetime
    "class": [0], # Must go to ground floor for in person class
    "sleep": [], # Sleep only happens at person's home floor
    "meal": [0], # Must go to ground floor to eat out / pickup food
    "exercise": [0], # Send to ground floor
    "shop": [0], # Must go to ground floor to go to store
    "chores": [], # Chores only happen at person's home floor
    "study": [0], # Send to ground floor
}
simple_elevator_algorithm = "stay_where_stopped"
simple_elevator_starting_floors = [0, 0] # Two elevators, both starting at ground floor
simple_elevator_capacities = [10, 10, 10]
simple_elevator_steps_per_stops = [5, 5, 5] # Num simulation steps an elevator must pass (doing nothing) each time it stops to onload or offload passengers
simple_elevator_return_to_floors = [1, 1, 1]

class TestSimulation(unittest.TestCase):
    """
    Before each test, generate a Building
    """
    def setUp(self):
        # Runs before each test
        self.building = Building(simple_floor_populations, simple_dest_floors_by_state_name, simple_elevator_algorithm, simple_elevator_starting_floors, simple_elevator_capacities, simple_elevator_steps_per_stops, simple_elevator_return_to_floors)

    """
    state_change_going_down(building, floor_id, person):
    
    Moves a person from people_on_floor to people_going_down and, if it isn't already,
    sets is_down_pressed to True and adds the floor to floors_new_down_button_pressed
    """
    def test_state_change_going_down(self):
        test_floor = 1
        person = self.building.floors[test_floor].people_on_floor[0] # Grab the only person on the 2nd floor
        Simulation.state_change_going_down(self.building, test_floor, person)

        self.assertEqual(0, len(self.building.floors[test_floor].people_on_floor))
        self.assertEqual(person, self.building.floors[test_floor].people_going_down[0])
        self.assertTrue(self.building.floors[test_floor].is_down_pressed)
        self.assertEqual(test_floor, self.building.floors_new_down_button[0])
        return

    """
    state_change_going_up(building, floor_id, person):
    
    Moves a person from people_on_floor to people_going_up and, if it isn't already,
    sets is_up_pressed to True and adds the floor to floors_new_down_button_pressed
    """
    def test_state_change_going_up(self):
        test_floor = 0
        person = self.building.floors[test_floor].people_on_floor[0] # Grab the only person on the 1nd floor
        Simulation.state_change_going_up(self.building, test_floor, person)

        self.assertEqual(0, len(self.building.floors[test_floor].people_on_floor))
        self.assertEqual(person, self.building.floors[test_floor].people_going_up[0])
        self.assertTrue(self.building.floors[test_floor].is_up_pressed)
        self.assertEqual(test_floor, self.building.floors_new_up_button[0])
        return

    """
    Asserts that handle_state_change correctly updates a Building when a Person needs to change state.
    """
    def test_handle_state_change_scheduled(self):
        day = 0
        home_floor_id = 1
        person = self.building.floors[home_floor_id].people_on_floor[0] # Only person on 2nd floor
        person.state_change_ids[day][0] = (2, 1) # Set first state change to change from sleep to class
        person.dest_floors_by_state_name["class"] = [0] # Ensure that the only dest floor for class for this person is 1st floor
        
        # Ensure the test data we just set is properly reflected within the Building
        self.assertEqual(2, self.building.floors[home_floor_id].people_on_floor[0].state_change_ids[day][0, 0])
        self.assertEqual(1, self.building.floors[home_floor_id].people_on_floor[0].state_change_ids[day][0, 1])
        self.assertEqual([0], self.building.floors[home_floor_id].people_on_floor[0].dest_floors_by_state_name["class"])

        Simulation.handle_state_change_scheduled(self.building, day, person) # The function we are testing
        # What should happen: Person needs to travel down to first floor. Person should be removed from people_on_floor and added to people_going_down on the same floor.
        # This is the first person to be added to people_going_down, so the floor's is_down_pressed should be updated and the floor id should be added to the building's floors_new_down_button.
        self.assertEqual([], self.building.floors[home_floor_id].people_on_floor)
        self.assertEqual(1, len(self.building.floors[home_floor_id].people_going_down))
        self.assertEqual(person, self.building.floors[home_floor_id].people_going_down[0])
        self.assertEqual(True, self.building.floors[home_floor_id].is_down_pressed)
        self.assertEqual(home_floor_id, self.building.floors_new_down_button[0])
        
        return 

    # Covered by test above
    def test_handle_state_changes_scheduled(self):
        return

    def test_handle_state_changes_randomly(self):
        return

    """
    increment_counters(building, day):

    Ensures that increment_counters increments the waiting_counters, riding_counters for applicable Persons and increments active_counters, idle_counters for applicable Elevators. 
    """
    def test_increment_counters(self):
        day = 0 # increment_counters takes a day argument so it can store different counters for each day of the week
        person_waiting_floor = 0
        person_riding_floor = 1
        active_elevator = 0
        idle_elevator = 1

        # Set one person to be waiting for an elevator
        person = self.building.floors[person_waiting_floor].people_on_floor[0]
        self.building.floors[person_waiting_floor].people_going_up.append(person)
        self.building.floors[person_waiting_floor].people_on_floor.remove(person)

        # Set one person to be riding on an elevator
        person = self.building.floors[person_riding_floor].people_on_floor[0]
        self.building.elevators[active_elevator].people_by_destination[person_waiting_floor] = [person]
        self.building.floors[person_riding_floor].people_on_floor.remove(person)
        
        # Set one elevator to be active
        self.building.elevators[active_elevator].is_moving = True
        
        # Set one elevator to be idle (False is default value so this is kind of pointless)
        self.building.elevators[idle_elevator].is_moving = False

        Simulation.increment_counters(self.building, day)

        # Check all four counters got incremented where applicable
        person_waiting = self.building.floors[person_waiting_floor].people_going_up[0]
        self.assertTrue(([1, 1] == person_waiting.waiting_counters).all())

        person_riding = self.building.elevators[active_elevator].people_by_destination[person_waiting_floor][0]
        self.assertTrue(([1, 1] == person_riding.riding_counters).all())

        self.assertTrue(([1, 1] == self.building.elevators[idle_elevator].idle_counters).all())
        self.assertTrue(([1, 1] == self.building.elevators[active_elevator].active_counters).all())
        return

    """
    handle_new_up_button_presses(building):

    For each floor in floors_new_up_button, the Building's elevator_algorithm is used to assign it to one of the Elevator's up_stops list
    """
    def test_handle_new_up_button_presses(self):
        # Test built for the SWS algorithm:
        # Both elevators are idle, one on 1st floor and one on 2nd floor. The up button on the first floor is pushed. The idle elevator on the 1st floor should be assigned this up_stop.
        self.building.elevators[1].cur_floor = 1
        self.building.floors_new_up_button.append(0)
        Simulation.handle_new_up_button_presses(self.building)
        
        self.assertEqual(0, self.building.elevators[0].up_stops[0])
        return

    """
    handle_new_down_button_presses(building):

    For each floor in floors_new_down_button, the Building's elevator_algorithm is used to assign it to one of the Elevator's down_stops list
    """
    def test_handle_new_down_button_presses(self):
        # Test built for the SWS algorithm:
        # Both elevators are idle, one on 1st floor and one on 2nd floor. The down button on the 2nd floor is pushed. The idle elevator on the 2nd floor should be assigned this down_stop.
        self.building.elevators[1].cur_floor = 1
        self.building.floors_new_down_button.append(1)
        Simulation.handle_new_down_button_presses(self.building)
        
        self.assertEqual(1, self.building.elevators[1].down_stops[0])
        return
    """
    handle_new_button_presses(building):

    Calls handle_new_down_button_presses(building) and handle_new_up_button_presses(building)
    """
    def test_handle_new_button_presses(self):
        return

    def test_handle_onboard_up(self):
        return

    def test_handle_onboard_down(self):
        return
        
    """
    handle_onboard(building, elevator):

    Moves people from people_going_up and people_going_down lists to an Elevator's people_by_destination dictionary.
    Also updates the Elevator's up_stops or down_stops to include the destinations of the people onboarding.
    """
    def test_handle_onboard(self):
        # Person wanting to going up from 1st to 2nd floor
        person_going_up = self.building.floors[0].people_on_floor[0]
        person_going_up.dest_floor = 1
        self.building.floors[0].people_on_floor.remove(person_going_up)
        self.building.floors[0].people_going_up.append(person_going_up)
        # Person wanting to go down from 2nd to 1st floor
        person_going_down = self.building.floors[1].people_on_floor[0]
        person_going_down.dest_floor = 0
        self.building.floors[1].people_on_floor.remove(person_going_down)
        self.building.floors[1].people_going_down.append(person_going_down)
        # Elevator on 1st floor going up
        self.building.elevators[0].cur_floor = 0
        self.building.elevators[0].is_moving = True
        self.building.elevators[0].is_moving_up = True
        # Elevator on 2nd floor going down
        self.building.elevators[1].cur_floor = 1
        self.building.elevators[1].is_moving = True
        self.building.elevators[1].is_mocing_up = False

        Simulation.handle_onboard(self.building, self.building.elevators[0])
        Simulation.handle_onboard(self.building, self.building.elevators[1])

        # 1st floor people_going_up should be empty since Elevator 0 picked them up (moved into Elevator's people_by_destination dictionary)
        self.assertEqual(0, len(self.building.floors[0].people_going_up))
        self.assertEqual(person_going_up, self.building.elevators[0].people_by_destination[person_going_up.dest_floor][0])
        # The Person's destination floor should have been added to Elevator 0's up_stops
        self.assertEqual(1, len(self.building.elevators[0].up_stops))
        self.assertEqual(person_going_up.dest_floor, self.building.elevators[0].up_stops[0])
        # 2nd floor people_going_down should be empty since Elevator 1 picked them up
        self.assertEqual(0, len(self.building.floors[1].people_going_down))
        self.assertEqual(person_going_down, self.building.elevators[1].people_by_destination[person_going_down.dest_floor][0])
        # The Person's destination floor should have been added to Elevator 1's down_stops
        self.assertEqual(1, len(self.building.elevators[1].down_stops))
        self.assertEqual(person_going_down.dest_floor, self.building.elevators[1].down_stops[0])


        return
    
    """
    handle_offload(building, elevator):

    Moves people from an Elevator's people_by_destination dictionary to the Elevator's current Floor's people_on_floor list.
    """
    def test_handle_offload(self):
        # Person wanting to offload on 1st Floor and Elevator currently on 1st Floor
        person1 = self.building.floors[0].people_on_floor[0]
        self.building.floors[0].people_on_floor.remove(person1)
        self.building.elevators[0].cur_floor = 0
        self.building.elevators[0].people_by_destination[0] = [person1]
        # Person wanting to offload on 2nd Floor and Elevator currently on 2nd Floor
        person2 = self.building.floors[1].people_on_floor[0]
        self.building.floors[1].people_on_floor.remove(person2)
        self.building.elevators[1].cur_floor = 1
        self.building.elevators[1].people_by_destination[1] = [person2]

        Simulation.handle_offload(self.building, self.building.elevators[0])
        Simulation.handle_offload(self.building, self.building.elevators[1])
        # Person should have been removed from 1st Floor Elevator's people_by_destination dictionary and added to the 1st Floor's people_on_floor list
        self.assertEqual(0, len(self.building.elevators[0].people_by_destination[0]))
        self.assertEqual(person1, self.building.floors[0].people_on_floor[0])
        # Person should have been removed from 2nd Floor Elevator's people_by_destination dictionary and added to the 2nd Floor's people_on_floor list
        self.assertEqual(0, len(self.building.elevators[1].people_by_destination[1]))
        self.assertEqual(person2, self.building.floors[1].people_on_floor[0])
        return

    def test_update_returning_elevators(self):
        self.assertEqual("not", "implemented")
        return
    
    def test_handle_active_elevator_state_change(self):
        self.assertEqual("not", "implemented")
        return

    """
    Asserts that update_active_up_elevator correctly updates an active Elevator.
    """
    def test_update_active_up_elevator(self):
        # Test Elevator's cur_floor is not within its up_stops. (When an Elevator is not on a Floor in up_stops, it moves one Floor closer,
        # but does not update anything else until the next update)
        up_elevator = self.building.elevators[0]
        up_elevator.is_active = True
        up_elevator.is_moving_up = True
        up_elevator.is_loading = False
        up_elevator.is_returning = False
        
        up_elevator.cur_floor = 0
        up_elevator.up_stops.append(1)

        Simulation.update_active_up_elevator(self.building, up_elevator) # This should move the elevator from 1st to 2nd floor (0 to 1 idxs)
        self.assertEqual(1, up_elevator.cur_floor) # Elevator's cur_floor should be the 2nd floor
        self.assertEqual(1, up_elevator.up_stops[0]) # 2nd floor should still be in up_stops
        self.assertTrue(([0, 0] == up_elevator.loading_counters).all()) # loading counters should be zero since Elevator hasn't loading yet

        Simulation.update_active_up_elevator(self.building, up_elevator) # This should handle and remove 2nd floor from up_stops (register that the Elevator has loading on the Floor)
        self.assertTrue(up_elevator.is_loading)
        self.assertFalse(up_elevator.is_active)
        self.assertEqual(up_elevator.loading_steps, up_elevator.steps_per_stop) # The Elevator loading, so loading_steps should have been set
        self.assertEqual(0, len(up_elevator.up_stops)) # Stops get removed from up_stops as soon as they are handled
        self.assertTrue(([1, 1] == up_elevator.loading_counters).all()) # loading counters should have been incremented

        Simulation.update_active_up_elevator(self.building, up_elevator) # This should decrement loading_steps
        self.assertEqual(up_elevator.steps_per_stop - 1, up_elevator.loading_steps) # loading_steps should be one less than steps_per_stop since it got decremented
        self.assertTrue(([2, 2] == up_elevator.loading_counters).all()) # loading counters should have been incremented again
        up_elevator.loading_steps = 1 # Set loading_steps to only 1 step remaining

        Simulation.update_active_up_elevator(self.building, up_elevator) # Should set Elevator to be idle since it has no more up_stops or down_stops
        self.assertTrue(up_elevator.is_idle)
        self.assertFalse(up_elevator.is_active)
        self.assertFalse(up_elevator.is_loading)
        self.assertFalse(up_elevator.is_returning)

        return

    """
    Asserts that update_active_down_elevator correctly updates an active Elevator.
    """
    def test_update_active_down_elevator(self):
        # Test Elevator's cur_floor is not within its down_stops. (When an Elevator is not on a Floor in down_stops, it moves one Floor closer,
        # but does not update anything else until the next update)
        down_elevator = self.building.elevators[0]
        down_elevator.is_active = True
        down_elevator.is_moving_up = False
        down_elevator.is_loading = False
        down_elevator.is_returning = False

        down_elevator.cur_floor = 1
        down_elevator.down_stops.append(0)

        Simulation.update_active_down_elevator(self.building, down_elevator) # This should move the elevator from 2nd to 1st floor (1 to 0 idxs)
        self.assertEqual(0, down_elevator.cur_floor) # Elevator's cur_floor should be the 1st floor
        self.assertEqual(0, down_elevator.down_stops[0]) # 1st floor should still be in down_stops
        self.assertTrue(([0, 0] == down_elevator.loading_counters).all()) # loading counters should be zero since Elevator hasn't loading yet

        Simulation.update_active_down_elevator(self.building, down_elevator) # This should handle and remove 1st floor from down_stops
        self.assertTrue(down_elevator.is_loading)
        self.assertFalse(down_elevator.is_active)
        self.assertEqual(down_elevator.loading_steps, down_elevator.steps_per_stop) # The Elevator loading, so loading_steps should have been set
        self.assertEqual(0, len(down_elevator.up_stops)) # Stops get removed from down_stops as soon as they are handled
        self.assertTrue(([1, 1] == down_elevator.loading_counters).all()) # loading counters should have been incremented

        Simulation.update_active_down_elevator(self.building, down_elevator) # This should decrement loading_steps
        self.assertEqual(down_elevator.steps_per_stop - 1, down_elevator.loading_steps) # loading_steps should be one less than steps_per_stop since it got decremented
        self.assertTrue(([2, 2] == down_elevator.loading_counters).all()) # loading counters should have been incremented again
        down_elevator.loading_steps = 1 # Set loading_steps to only 1 step remaining

        Simulation.update_active_down_elevator(self.building, down_elevator) # Should set Elevator to be idle since it has no more down_stops or up_stops
        self.assertTrue(down_elevator.is_idle)
        self.assertFalse(down_elevator.is_active)
        self.assertFalse(down_elevator.is_loading)
        self.assertFalse(down_elevator.is_returning)

        return

    # Covered by the two test above
    def test_update_active_elevators(self):
        return

    """
    Asserts that update_idle_elevators correctly updates an idle Elevators.
    """
    def test_update_idle_elevators(self):
        up_elevator = self.building.elevators[0]
        down_elevator = self.building.elevators[1]

        up_elevator.up_stops.append(1)
        down_elevator.down_stops.append(0)

        Simulation.update_idle_elevators(self.building, self.building.elevators)

        self.assertTrue(up_elevator.is_active)
        self.assertTrue(up_elevator.is_moving_up)
        self.assertFalse(up_elevator.is_idle)
        self.assertFalse(up_elevator.is_loading)
        self.assertFalse(up_elevator.is_returning)

        self.assertTrue(down_elevator.is_active)
        self.assertFalse(down_elevator.is_moving_up)
        self.assertFalse(up_elevator.is_idle)
        self.assertFalse(up_elevator.is_loading)
        self.assertFalse(up_elevator.is_returning)
        return
    
    # Covered by two tests above
    def update_elevators(self):
        return 