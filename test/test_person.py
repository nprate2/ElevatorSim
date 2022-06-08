
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
    """
    Before each test, generate a list of 10 Persons
    """
    @classmethod
    def setUpClass(self):
        self.people = []
        for i in (range(10)):
            person = Person(id=i, home_floor=i, prob_having_visitors=0, avg_num_visitors=0, building_dest_floors_by_state_name=test_dest_floors_by_state_name)
            person.steps_waiting[0] = i
            person.steps_traveling[0] = i
        return

    """
    Assert the Person() constructor produces a Person as expected.
    """
    def test_generation(self):
        for i in (range(len(self.people))):
            self.assertEqual(i, self.people[i].id)
            self.assertEqual(i, self.people[i].home_floor)
            self.assertEqual(i, self.people[i].cur_floor)
            self.assertEqual(i, self.people[i].prob_having_visitors)
            self.assertEqual(i, self.people[i].avg_num_visitors)
            self.assertEqual(i, self.people[i].steps_waiting[0])
            self.assertEqual(i, self.people[i].steps_traveling[0])

            # Length of state change steps and state change ids should be equal, since each id corresponds to a state change
            self.assertEqual(len(self.people[i].state_change_steps), len(self.people[i].state_change_ids))
    """
    Assert that state_change_steps, state_change_ids, and schedule use unique memory for each Person
    """
    def test_unique_memory(self):
        # Ensure all fields are still set to i after multiple people are generated. Also check that class, sleep, meal, exercise, chores, and study states within dest floors contain i (since i is the home floor)
        for i in range(len(self.people)):
            # Unless memory is not unique, self.people will always have unique state change steps and corresponding ids, as well as unique schedules
            self.assertFalse(np.array_equal(self.people[i].state_change_steps, self.people[i-1].state_change_steps))
            self.assertFalse(np.array_equal(self.people[i].state_change_ids, self.people[i-1].state_change_ids))
            self.assertFalse(np.array_equal(self.people[i].schedule, self.people[i-1].schedule))

    """
    Assert that generate_state_change_data() performs as expected.
    """
    def test_generate_state_change_data(self):
        # Test a super simplified schedule case
        simple_schedule = np.zeros((2, 2))
        simple_schedule[0][0] = 1
        # This simple schedule has one state change on the first day (1 to 0), and no state changes on the second day (all 0's)
        person = Person(id=1, home_floor=1, prob_having_visitors=1, avg_num_visitors=1, building_dest_floors_by_state_name=test_dest_floors_by_state_name)
        person.schedule = simple_schedule
        person.generate_state_change_data()

        # Ensure the first day has one generated state_change_steps and state_change_ids
        self.assertEqual(1, len(person.state_change_steps[0]))
        self.assertEqual(1, len(person.state_change_ids[0]))
        # Ensure the state_change_ids are correct, i.e. the state changes from 1 to 0
        self.assertEqual(1, person.state_change_ids[0][0][0])
        self.assertEqual(0, person.state_change_ids[0][0][1])
        # Ensure the second day has zero generated state_change_steps and state_change_ids
        self.assertEqual(0, len(person.state_change_steps[1]))
        self.assertEqual(0, len(person.state_change_ids[1]))


        # Test a normally generated Schedule case
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

        # Now we know the number of generated state changes is correct, let's ensure the content is accurate too
        cur_state = person.schedule[0,0]
        for day in range(person.schedule.shape[0]):
            num_state_changes = 0
            for chunk in range(person.schedule.shape[1]):
                if person.schedule[day, chunk] != cur_state:
                    self.assertEqual(cur_state, person.state_change_ids[day][num_state_changes][0])
                    self.assertEqual(person.schedule[day, chunk], person.state_change_ids[day][num_state_changes][1])

                    cur_state = person.schedule[day, chunk]
                    num_state_changes += 1

        return
    
    """
    Assert that generate_dest_floors_by_state_name performs as expected.
    """
    def test_generate_dest_floors_by_state_name(self):
        for i in range(len(self.people)):
            # Tests that a Person's home floor is one of the destinations for various states
            self.assertEqual(self.people[i].home_floor, self.people[i].dest_floors_by_state_name["class"])
            self.assertEqual(self.people[i].home_floor, self.people[i].dest_floors_by_state_name["sleep"])
            self.assertEqual(self.people[i].home_floor, self.people[i].dest_floors_by_state_name["meal"])
            self.assertEqual(self.people[i].home_floor, self.people[i].dest_floors_by_state_name["exercise"])
            self.assertEqual(self.people[i].home_floor, self.people[i].dest_floors_by_state_name["chores"])
            self.assertEqual(self.people[i].home_floor, self.people[i].dest_floors_by_state_name["study"])
        return