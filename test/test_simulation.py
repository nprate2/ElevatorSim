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
simple_elevator_starting_floors = [0, 0] # Two elevators, both starting at ground floor
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

    def test_handle_state_change(self):
        day = 0
        home_floor_id = 1
        person = self.building.floors[home_floor_id].people_on_floor[0] # Only person on 2nd floor
        person.state_change_ids[day][0] = (2, 1) # Set first state change to change from sleep to class
        person.dest_floors_by_state_name["class"] = [0] # Ensure that the only dest floor for class for this person is 1st floor
        
        # Ensure the test data we just set is properly reflected within the Building
        self.assertEqual(2, self.building.floors[home_floor_id].people_on_floor[0].state_change_ids[day][0, 0])
        self.assertEqual(1, self.building.floors[home_floor_id].people_on_floor[0].state_change_ids[day][0, 1])
        self.assertEqual([0], self.building.floors[home_floor_id].people_on_floor[0].dest_floors_by_state_name["class"])

        Simulation.handle_state_change(self.building, day, person) # The function we are testing
        # What should happen: Person needs to travel down to first floor. Person should be removed from people_on_floor and added to people_going_down on the same floor.
        # This is the first person to be added to people_going_down, so the floor's is_down_pressed should be updated and the floor id should be added to the building's floors_new_down_button.
        self.assertEqual([], self.building.floors[home_floor_id].people_on_floor)
        self.assertEqual(1, len(self.building.floors[home_floor_id].people_going_down))
        self.assertEqual(person, self.building.floors[home_floor_id].people_going_down[0])
        self.assertEqual(True, self.building.floors[home_floor_id].is_down_pressed)
        self.assertEqual(home_floor_id, self.building.floors_new_down_button[0])
        
        return 

    # Covered by test above
    def test_handle_state_changes(self):
        return

    """
    update_counters(building, day):

    Increments the steps_waiting, steps_traveling counters for applicable Persons and increments steps_active, steps_idle counters for applicable Elevators
    """
    def test_update_counters(self):
        day = 0 # update_counters takes a day argument so it can store different counters for each day of the week
        waiting_floor = 0
        traveling_floor = 1
        active_elevator = 0
        idle_elevator = 1

        print("\nHERE")
        print(len(self.building.floors))
        print(len(self.building.floors[0].people_on_floor))
        print("\n")
        # Set one person to be waiting for an elevator
        person = self.building.floors[waiting_floor].people_on_floor[0]
        self.building.floors[waiting_floor].people_going_up.append(person)
        self.building.floors[waiting_floor].people_on_floor.remove(person)

        # Set one person to be traveling on an elevator
        person = self.building.floors[traveling_floor].people_on_floor[0]
        self.building.elevators[active_elevator].people_by_destination[waiting_floor] = [person]
        self.building.floors[traveling_floor].people_on_floor.remove(person)
        
        # Set one elevator to be active
        self.building.elevators[active_elevator].is_moving = True
        
        # Set one elevator to be idle (False is default value so this is kind of pointless)
        self.building.elevators[idle_elevator].is_moving = False

        Simulation.update_counters(self.building, day)

        # Check all four counters got incremented where applicable
        waiting_person = self.building.floors[waiting_floor].people_going_up[0]
        self.assertEqual(1, waiting_person.steps_waiting[day])

        traveling_person = self.building.elevators[active_elevator].people_by_destination[waiting_floor][0]
        self.assertEqual(1, traveling_person.steps_traveling[day])

        self.assertEqual(1, self.building.elevators[idle_elevator].steps_idle[day])
        self.assertEqual(1, self.building.elevators[active_elevator].steps_active[day])
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

    """
    handle_onboard(building, elevator):

    Moves people from people_going_up and people_going_down lists to an Elevator's people_by_destination dictionary.
    Also updates the Elevator's up_stops or down_stops to include the destinations of the people onboarding.
    """
    def test_handle_onboard(self):
        person_going_up = self.building.floors[0].people_on_floor[0]
        person_going_up.dest_floor = 1
        self.building.floors[0].people_on_floor.remove(person_going_up)
        self.building.floors[0].people_going_up.append(person_going_up)

        person_going_down = self.building.floors[1].people_on_floor[0]
        person_going_down.dest_floor = 0
        self.building.floors[1].people_on_floor.remove(person_going_down)
        self.building.floors[1].people_going_down.append(person_going_down)

        self.building.elevators[0].cur_floor = 0
        self.building.elevators[0].is_moving = True
        self.building.elevators[0].is_moving_up = True

        self.building.elevators[1].cur_floor = 1
        self.building.elevators[1].is_moving = True
        self.building.elevators[1].is_mocing_up = False

        Simulation.handle_onboard(self.building, self.building.elevators[0])
        Simulation.handle_onboard(self.building, self.building.elevators[1])

        self.assertEqual(0, len(self.building.floors[0].people_going_up))
        self.assertEqual(person_going_up, self.building.elevators[0].people_by_destination[person_going_up.dest_floor][0])
        self.assertEqual(person_going_up.dest_floor, self.building.elevators[0].up_stops[0])

        self.assertEqual(0, len(self.building.floors[1].people_going_down))
        self.assertEqual(person_going_down, self.building.elevators[1].people_by_destination[person_going_down.dest_floor][0])
        self.assertEqual(person_going_down.dest_floor, self.building.elevators[1].down_stops[0])


        return
    
    """
    handle_offload(building, elevator):

    Moves people from an Elevator's people_by_destination dictionary to the Elevator's current Floor's people_on_floor list.
    """
    def test_handle_offload(self):
        person1 = self.building.floors[0].people_on_floor[0]
        self.building.floors[0].people_on_floor.remove(person1)
        self.building.elevators[0].cur_floor = 0
        self.building.elevators[0].people_by_destination[0] = [person1]

        person2 = self.building.floors[1].people_on_floor[0]
        self.building.floors[1].people_on_floor.remove(person2)
        self.building.elevators[1].cur_floor = 1
        self.building.elevators[1].people_by_destination[1] = [person2]

        Simulation.handle_offload(self.building, self.building.elevators[0])
        Simulation.handle_offload(self.building, self.building.elevators[1])

        self.assertEqual(0, len(self.building.elevators[0].people_by_destination.keys()))
        self.assertEqual(person1, self.building.floors[0].people_on_floor[0])
        self.assertEqual(0, len(self.building.elevators[1].people_by_destination.keys()))
        self.assertEqual(person2, self.building.floors[1].people_on_floor[0])
        return

    def test_update_active_up_elevator(self):
        return
    def test_update_active_down_elevator(self):
        return
    def test_update_active_elevators(self):
        return

    def test_update_idle_elevators(self):
        return
    
    # Covered by two tests above
    def update_elevators(self):
        return 