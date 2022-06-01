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
