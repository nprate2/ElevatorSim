from copy import deepcopy
from Floor import Floor
from Elevator import Elevator
from ElevatorAlgorithm import ElevatorAlgorithm

class Building:
    # (Unchanging) Used to define the physical structure of the building.
    floors = []
    elevators = []
    
    # Brains of the elevator system. Utilizes elevators list to schedule routes to visit floors with pressed "call elevator" buttons.
    elevator_algorithm = None

    # (Changing) Used to keep track of which floors have a "call elevator" button pressed that hasn't been assigned to an elevator yet.
    floors_new_up_button = []
    floors_new_down_button = []

    """
    Initializes a Building object.

    Takes:
    floor_populations - list of integers representing the number of residents on each Floor.
    building_dest_floors_by_state_name - dictionary where keys are strings representing state names for Persons and values are lists of integers representing Floor ids that said state can occur on.
    elevator_algorithm - string representing the scheduling algorithm to be used within the Building
    elevator_starting_floors - list of integers representing Floor ids where each Elevator will "begin" at the start of the simulation.
    elevator_capacities - list of integers representing the maximum amount of Persons that can be onboard each Elevator at any given time.
    elevator_steps_per_stops - list of integers representing the number of steps each Elevator takes to onload/offload/stop at a floor.
    """
    def __init__(self, floor_populations, building_dest_floors_by_state_name, elevator_algorithm, elevator_starting_floors, elevator_capacities, elevator_steps_per_stops):
        self.floors = deepcopy(self.floors)
        self.elevators = deepcopy(self.elevators) 
        self.floors_new_down_button = deepcopy(self.floors_new_down_button)
        self.floors_new_up_button = deepcopy(self.floors_new_up_button)
        
        self.generate_floors(floor_populations, building_dest_floors_by_state_name)
        self.generate_elevators(elevator_starting_floors, elevator_capacities, elevator_steps_per_stops)
        self.elevator_algorithm = ElevatorAlgorithm(elevator_algorithm)

    """
    Generates a list of Floor classes for the building.

    Takes:
    floor_populations - list of integers representing the number of residents on each floor of a building
    building_dest_floors_by_state_name - Passed to Person classes as generated by Floor classes. See "generate_dest_floors_by_state_name" within the Person class for more documentation.
    
    """
    def generate_floors(self, floor_populations, building_dest_floors_by_state_name):
        for i in range(len(floor_populations)):
            floor = Floor(id=i, num_residents=floor_populations[i], building_dest_floors_by_state_name=building_dest_floors_by_state_name)
            self.floors.append(floor)

    """
    Generates a list of Elevator classes for the building.

    Takes:
    elevator_starting_floors - list of integers representing starting Floor id of each elevator in a Building.
    elevator_capacities - list of integers representing the maximum amount of Persons that can be onboard each Elevator at any given time.
    elevator_steps_per_stops - list of integers representing the number of steps each Elevator takes to onload/offload/stop at a floor.
    """
    def generate_elevators(self, elevator_starting_floors, elevator_capacities, elevator_steps_per_stops):
        for i in range(len(elevator_starting_floors)):
            self.elevators.append(Elevator(id=i, capacity=elevator_capacities[i], starting_floor=elevator_starting_floors[i], steps_per_stop=elevator_steps_per_stops[i]))
            # Initialize each Elevator's people_by_destination dictionary with deepcopied empty lists (can't do this within an Elevator class because it doesn't know how many floors there are)
            for j in range(len(self.floors)):
                self.elevators[i].people_by_destination[j] = deepcopy([])

    """
    Prints the state of a building for debugging purposes.
    """
    def print_building_state(self):
        print("\n-----FLOORS-----\n")
        for i in range(len(self.floors)):
            print("Floor:", i)
            print("People on floor:", len(self.floors[i].people_on_floor))
            print("People going up:", len(self.floors[i].people_going_up))
            print("People going down:", len(self.floors[i].people_going_down))
            print("\n")
        
        print("\n-----ELEVATORS-----\n")
        for i in range(len(self.elevators)):
            print("Elevator:", i)
            print("Cur floor:", self.elevators[i].cur_floor)
            print("Is moving:", self.elevators[i].is_moving)
            print("Is moving up:", self.elevators[i].is_moving_up)
            print("Up stops:", self.elevators[i].up_stops)
            print("Down stops:", self.elevators[i].down_stops)
            print("\n")
            
