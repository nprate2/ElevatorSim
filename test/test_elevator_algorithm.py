import unittest

from src_imports import Building


simple_floor_populations = [1, 1, 1] # Two floor building with one resident on each floor
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
simple_elevator_starting_floors = [0, 1, 2] # Three elevators, one starting on each floor
simple_elevator_capacities = [10, 10, 10]
simple_elevator_steps_per_stops = [5, 5, 5] # Num simulation steps an elevator must pass (doing nothing) each time it stops to onload or offload passengers


class TestElevatorAlgorithm(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #self.building = Building(simple_floor_populations, simple_dest_floors_by_state_name, simple_elevator_starting_floors, simple_elevator_capacity, simple_elevator_algorithm, simple_elevator_steps_per_stop)
        return
    
    """
    Assert the "stay_where_stopped" scheduling algorithm behaves as expected.
    """
    def test_assign_stop_SWS(self):
        # Test that an idle Elevator on a floor gets assigned the stop
        building = Building(simple_floor_populations, simple_dest_floors_by_state_name, simple_elevator_algorithm, simple_elevator_starting_floors, simple_elevator_capacities, simple_elevator_steps_per_stops)
        building.elevator_algorithm.assign_stop(building.elevators, 0, "up")
        building.elevator_algorithm.assign_stop(building.elevators, 1, "down")
        self.assertEqual(1, len(building.elevators[0].up_stops))
        self.assertEqual(0, building.elevators[0].up_stops[0])
        self.assertEqual(1, len(building.elevators[1].down_stops))
        self.assertEqual(1, building.elevators[1].down_stops[0])

        # Test that closest active Elevator moving towards gets assigned the stop (if Elevator on requested floor is moving, it won't get assigned because the request was "too late")
        building = Building(simple_floor_populations, simple_dest_floors_by_state_name, simple_elevator_algorithm, simple_elevator_starting_floors, simple_elevator_capacities, simple_elevator_steps_per_stops)
        building.elevators[0].is_moving = True
        building.elevators[0].is_moving_up = True
        building.elevators[1].is_moving = True
        building.elevators[1].is_moving_up = True
        building.elevator_algorithm.assign_stop(building.elevators, 1, "up")
        self.assertEqual(1, len(building.elevators[0].up_stops))
        self.assertEqual(1, building.elevators[0].up_stops[0])

        return
    
    """
    Assert the "return_to_ground" scheduling algorithm behaves as expected.
    """
    def test_assign_stop_RTG(self):
        return