from copy import deepcopy
from distutils.command import build
from Person import Person

class Floor:
    id = -1
    num_residents = -1
    is_up_pressed = False
    is_down_pressed = False
    people_on_floor = []
    people_going_up = []
    people_going_down = []
    
    """
    Initializes a Floor class by setting id and num_residents, deepcopying lists to ensure unique memory between instances, and generating People to populate people_on_floor

    Takes:
    id - integer representing id of the Floor
    num_residents - integer representing number of residents of the Floor
    building_dest_floors_by_state_name - dictionary where keys are state names (strings) and values are lists of potential destination Floor ids for any given state from a Building's perspective
    
    Runs in O(P) time, where P is the number of People living on the Floor
    """
    def __init__(self, id, num_residents, building_dest_floors_by_state_name):
        # Ensure memory is unique per instance
        self.people_on_floor = deepcopy(self.people_on_floor)
        self.people_going_up = deepcopy(self.people_going_up)
        self.people_going_down = deepcopy(self.people_going_down)

        self.id = id
        self.num_residents = num_residents

        for i in range(num_residents):
            person_id = int(str(self.id) + str(i))
            prob_having_visitors = 0.25
            avg_num_visitors = 2

            person = Person(id=person_id, home_floor=self.id, prob_having_visitors=prob_having_visitors, avg_num_visitors=avg_num_visitors, building_dest_floors_by_state_name=building_dest_floors_by_state_name)
            self.people_on_floor.append(person)
