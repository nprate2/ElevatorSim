from copy import deepcopy
import numpy as np

class Elevator:
    id = -1
    capacity = -1
    steps_per_stop = 0

    cur_floor = -1
    is_moving = False
    is_moving_up = False
    stopped_steps = 0 # Used to keep an Elevator stationary when it stops to onload or offload Persons

    # When a Floor's new button press causes an Elevator to switch from idle to active, deidled_floor is set to this floor.
    deidled_floor = -1 # Used by ElevatorAlgorithm to avoid assigning stops to an Elevator until it reaches its deidled_floor (causes faults otherwise)
    deidled_floor_direction = "" # Used to remember what direction the Person on deidled_floor wants to travel (since the Elevator may have to travel in the opposite direction to reach deidled_floor)

    # Keys are Floor ids and values are lists of Persons who will get off the elevator at that floor.
    people_by_destination = {}
    
    # List of floors to stop at going up (includes destination floors and requested external stops where new people will get on elevator). Order of list does not represent stopping order.
    up_stops = []
    # List of floors to stop at going up (includes destination floors and requested external stops where new people will get on elevator). Order of list does not represent stopping order.
    down_stops = []

    # Arrays counting the number of simulation steps an Elevator spends idle and active
    steps_idle = np.zeros((7,))
    steps_active = np.zeros((7,))
    steps_stopped = np.zeros((7,))

    def __init__(self, id, capacity, starting_floor, steps_per_stop):
        self.id = id
        self.capacity = capacity
        self.cur_floor = starting_floor
        self.steps_per_stop = steps_per_stop
        # Ensure memory is unique per instance
        self.people_by_destination = deepcopy(self.people_by_destination)
        self.up_stops = deepcopy(self.up_stops)
        self.down_stops = deepcopy(self.down_stops)
        self.steps_idle = deepcopy(self.steps_idle)
        self.steps_active = deepcopy(self.steps_active)
        self.steps_stopped = deepcopy(self.steps_stopped)

        