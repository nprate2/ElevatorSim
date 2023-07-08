from copy import deepcopy
import numpy as np

class Elevator:
    id = -1
    capacity = -1
    steps_per_load = 0

    cur_floor = -1
    is_active = False
    is_idle = True
    is_loading = False
    is_returning = False

    #is_moving = False # Used to know if an Elevator is moving.
    is_moving_up = False # Used to know the direction of a moving Elevator.
    is_returning = False # Used to know if an Elevator is returning to a floor.
    loading_steps = 0 # Used to keep an Elevator stationary when it stops to onload or offload Persons

    # When a Floor's new button press causes an Elevator to switch from idle to active, deidled_floor is set to this floor.
    deidled_floor = -1 # Used by ElevatorAlgorithm to avoid assigning stops to an Elevator until it reaches its deidled_floor (causes faults otherwise)
    deidled_floor_direction = "" # Used to remember what direction the Person on deidled_floor wants to travel (since the Elevator may have to travel in the opposite direction to reach deidled_floor)

    # Used by Elevator's utilizing variants of the "return_to" algorithm, where Elevators are able to return to specific floors when they run out of stops.
    return_to_floor = -1

    # Keys are Floor ids and values are lists of Persons who will get off the elevator at that floor.
    people_by_destination = {}
    
    # List of floors to stop at going up (includes destination floors and requested external stops where new people will get on elevator). Order of list does not represent stopping order.
    up_stops = []
    # List of floors to stop at going up (includes destination floors and requested external stops where new people will get on elevator). Order of list does not represent stopping order.
    down_stops = []

    # Each counter is an array of two integers, tracking the number of simulation steps this Elevator spends in a particular state.
    # array[0] represents the daily count, array[1] represents the hourly count
    idle_counters = np.zeros((2,), dtype=int)
    active_counters = np.zeros((2,), dtype=int)
    loading_counters = np.zeros((2,), dtype=int)
    returning_counters = np.zeros((2,), dtype=int)

    """
    
    Takes:
    id - integer representing id of the Elevator
    capacity - integer representing capacity of the Elevator
    starting_floor - integer representing initial position of the Elevator at start of simulation
    steps_per_load - integer representing the number of simulation steps the Elevator takes to onload/offload Persons

    Runs in O(1) time.
    """
    def __init__(self, id, capacity, starting_floor, steps_per_load, return_to_floor):
        self.id = id
        self.capacity = capacity
        self.cur_floor = starting_floor
        self.steps_per_load = steps_per_load
        self.return_to_floor = return_to_floor
        
        # Ensure memory is unique per instance
        self.people_by_destination = deepcopy(self.people_by_destination)
        self.up_stops = deepcopy(self.up_stops)
        self.down_stops = deepcopy(self.down_stops)
        #self.counters = deepcopy(self.counters)
        self.idle_counters = deepcopy(self.idle_counters)
        self.active_counters = deepcopy(self.active_counters)
        self.loading_counters = deepcopy(self.loading_counters)
        self.returning_counters = deepcopy(self.returning_counters)

    """
    Sets the state of an Elevator to active.

    Takes:
    is_moving_up - Boolean representing whether the Elevator will move up or down
    """
    def set_state_active(self, is_moving_up):
        #print("Elevator " + str(self.id) + " set to active")
        self.is_active = True
        self.is_moving_up = is_moving_up

        self.is_idle = False
        self.is_loading = False
        self.is_returning = False

    """
    Sets the state of an Elevator to idle.
    """
    def set_state_idle(self):
        #print("Elevator " + str(self.id) + " set to idle")
        self.is_idle = True

        self.is_active = False
        self.is_loading = False
        self.is_returning = False

    """
    Sets the state of an Elevator to loading.
    """
    def set_state_loading(self):
        #print("Elevator " + str(self.id) + " set to loading")
        self.is_loading = True

        self.is_active = False
        self.is_idle = False
        self.is_returning = False

        self.loading_steps = self.steps_per_load # set loading_steps counter to know when loading terminates

    """
    Sets the state of an Elevator to returning.

    Takes:
    is_moving_up - Boolean representing whether the Elevator will move up or down
    """
    def set_state_returning(self, is_moving_up):
        print("Elevator " + str(self.id) + " set to returning")
        self.is_returning = True
        self.is_moving_up = is_moving_up

        self.is_active = False
        self.is_idle = False
        self.is_loading = False


        