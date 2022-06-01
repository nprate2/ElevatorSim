
"""
The Person class depends on the Schedule class.
"""
import unittest
import numpy as np
from tqdm import tqdm
from src_imports import Person

test_dest_floors_by_state_name = {
    "freetime": [],
    "class": [],
    "sleep": [],
    "meal": [],
    "exercise": [],
    "shop": [],
    "chores": [],
    "study": [],
}

class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #print("-----TESTING PERSON-----")
        return

    def test_generation(self):
        #print(".....generating 100 people.....")
        for i in (range(100)):
            person = Person(id=i, home_floor=i, prob_having_visitors=0, avg_num_visitors=0, building_dest_floors_by_state_name=test_dest_floors_by_state_name)
    
    def test_unique_memory(self):
        #print(".....testing unique memory.....")
        people = []
        # Set all fields to i and leave building dest floors empty for each state
        for i in range(10):
            person = Person(id=i, home_floor=i, prob_having_visitors=i, avg_num_visitors=i, building_dest_floors_by_state_name=test_dest_floors_by_state_name)
            person.steps_waiting[0] = i
            person.steps_traveling[0] = i
            people.append(person)

        # Ensure all fields are still set to i after multiple people are generated. Also check that class, sleep, meal, exercise, chores, and study states within dest floors contain i (since i is the home floor)
        for i in range(10):
            self.assertEqual(i, people[i].id)
            self.assertEqual(i, people[i].home_floor)
            self.assertEqual(i, people[i].prob_having_visitors)
            self.assertEqual(i, people[i].avg_num_visitors)
            self.assertEqual(i, people[i].steps_waiting[0])
            self.assertEqual(i, people[i].steps_traveling[0])
            self.assertEqual([i], people[i].dest_floors_by_state_name["class"])
            self.assertEqual([i], people[i].dest_floors_by_state_name["sleep"])
            self.assertEqual([i], people[i].dest_floors_by_state_name["meal"])
            self.assertEqual([i], people[i].dest_floors_by_state_name["exercise"])
            self.assertEqual([i], people[i].dest_floors_by_state_name["chores"])
            self.assertEqual([i], people[i].dest_floors_by_state_name["study"])
            # Length of state change steps and state change ids should be equal, since each id corresponds to a state change
            self.assertEqual(len(people[i].state_change_steps), len(people[i].state_change_ids))
            # Unless memory is not unique, people will always have unique state change steps and corresponding ids, as well as unique schedules
            self.assertFalse(np.array_equal(people[i].state_change_steps, people[i-1].state_change_steps))
            self.assertFalse(np.array_equal(people[i].state_change_ids, people[i-1].state_change_ids))
            self.assertFalse(np.array_equal(people[i].schedule, people[i-1].schedule))

    def test_generate_state_change_data(self):
        person = Person(id=1, home_floor=1, prob_having_visitors=1, avg_num_visitors=1, building_dest_floors_by_state_name=test_dest_floors_by_state_name)
        # For each state change in a person's schedule, there should be one change step and one change id
        cur_state = person.schedule[0,0]
        for day in range(person.schedule.shape[0]):
            num_state_changes = 0
            for chunk in range(person.schedule.shape[1]):
                if person.schedule[day, chunk] != cur_state:
                    cur_state = person.schedule[day, chunk]
                    num_state_changes += 1

            self.assertEqual(num_state_changes, len(person.state_change_steps[day]))
            self.assertEqual(num_state_changes, len(person.state_change_ids[day]))
        return
    
    # Covered within test_unique_memory
    def test_generate_dest_floors_by_state_name(self):
        return