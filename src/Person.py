from random import random
import numpy as np
from copy import deepcopy
import Schedule

class Person:
    id = -1
    home_floor = -1
    cur_floor = -1
    dest_floor = -1

    cur_num_visitors = 0
    prob_having_visitors = 0.0
    avg_num_visitors = -1

    #daily_steps_waiting = 0
    #hourly_steps_waiting = 0
    #daily_steps_riding = 0
    #hourly_steps_riding = 0

    # List of integers used to count simulation steps spent in various states
    # Idxs and uses: 0 - daily steps waiting, 1 - hourly steps waiting, 2 - daily steps riding,
    #                3 - hourly steps riding
    #counters = np.zeros((6,), dtype=int)
    waiting_counters = np.zeros((2,), dtype=int)
    riding_counters = np.zeros((2,), dtype=int)

    schedule = [] # Numpy array of shape (7, N) where N is the number of time chunks in a given day.
    state_change_steps = [] # Precise step numbers to change state. Idxs correspond to items in state_change_ids. Contains step numbers for the entire week, but steps are within a day
    state_change_ids = [] # Int tuples. (3, 4) means a state change from 3 to 4

    dest_floors_by_state_name = {} # Stores possible destination floors for each state of a Person. Keys are state names (strings) and values are lists of integers representing Floor ids

    """
    Initializes a Person class by setting id, home_floor, prob_having_visitors, avg_num_visitors, and avg_num_visitors.
    Generates a schedule for the Person then, using that schedule, generates state change data to determine exact steps for state changes in the simulation.
    Generates dest_floors_by_state_name by combining building_dest_floors_by_state_name with the Person's home_floor

    Takes:
    id - integer representing the id of the Person
    home_floor - integer representing the home Floor of the Person
    prob_having_visitors - float between 0.0 and 1.0 representing the probabilitiy of the Person to bring visitors back with them when they travel from the 1st floor
    avg_num_visitors - integer representing the average number of visitors the Person brings back with them
    building_dest_floors_by_state_name - dictionary where keys are state names (strings) and values are lists of potential destination Floor ids for any given state from a Building's perspective

    Runs in O(1) + O(generate_schedule) + O(generate_state_change_data) + O(generate_dest_floors_by_state_name):
    O(1) + + (O(D) + O(C^2)) + O(1)

    """
    def __init__(self, id, home_floor, prob_having_visitors, avg_num_visitors, building_dest_floors_by_state_name):
        self.id = id
        self.home_floor = home_floor
        self.cur_floor = home_floor
        self.prob_having_visitors = prob_having_visitors
        self.avg_num_visitors = avg_num_visitors

        # Ensure memory is unique per instance
        #self.steps_waiting = deepcopy(self.steps_waiting)
        #self.steps_riding = deepcopy(self.steps_riding)

        self.schedule = deepcopy(self.schedule)
        self.schedule = Schedule.generate_schedule()
        self.state_change_steps = deepcopy(self.state_change_steps)
        self.state_change_ids = deepcopy(self.state_change_ids)
        #self.counters = deepcopy(self.counters)
        self.waiting_counters = deepcopy(self.waiting_counters)
        self.riding_counters = deepcopy(self.riding_counters)

        self.generate_state_change_data()
        self.generate_dest_floors_by_state_name(building_dest_floors_by_state_name)

    """
    Computes state_change_steps and state_change_idx. These are used to store the exact step number that a person changes state, as well as what states they change between.
    state_change_steps[i] and state_change_ids[i] will be the same length, but that length may differ between i's, as it is dependent upon how many state changes a schedule has in a given day.
    
    Runs in O(D) + O(C^2) where D is the number of days in a schedule and C is the number of chunks in a day:
    """
    def generate_state_change_data(self):
        state_change_steps = []
        state_change_ids = []
        cur_state = self.schedule[0, 0]
        for day in range(self.schedule.shape[0]):
            daily_steps = []
            daily_ids = []
            # Each j represents 1 hour. 1hr = 3600s. 1 step = 3.5s. 3600/3.5 = 1028.5 steps
            for j in range(self.schedule.shape[1]):
                next_state = self.schedule[day, j]
                if next_state != cur_state:
                    true_step = 1028 * j
                    randomized_true_step = 0
                    if j == 0:
                        # Then we can't be early for state change (since daily step number would be negative, it starts at 0 each day), allow people to be twice as late
                        randomized_true_step = true_step + np.random.randint(0, 686)
                    else:
                        randomized_true_step = true_step + np.random.randint(-343, 343) # 343 is roughly 1/3 of an hour in steps, so people can be up to 20 mins early or late when switching activities
                    
                    daily_steps.append(randomized_true_step)
                    daily_ids.append((cur_state, next_state))
                    cur_state = next_state
            state_change_steps.append((np.asarray(daily_steps)))
            state_change_ids.append((np.asarray(daily_ids)))

        self.state_change_steps = (np.asarray(state_change_steps, dtype=object))
        self.state_change_ids = (np.asarray(state_change_ids, dtype=object))
        
        return

    """
    Sets dest_floors_by_state_name by adding the Person's home floor to the appropriate state's destination floors in building_dest_floors_by_state_name.

    Takes:
    building_dest_floors_by_state_name - Dictionary where keys are state names (strings) and values are lists of potential destination Floor ids for any given state from a Building's perspective (Building doesn't know the home floor of a Person)
    
    Runs in O(1)
    """
    def generate_dest_floors_by_state_name(self, building_dest_floors_by_state_name):
        self.dest_floors_by_state_name = deepcopy(building_dest_floors_by_state_name)
        
        # Check if various state names exist, and if so, add the person's home floor if it is not already present
        # If a state is not already in the keys, that means that state was not included in the simulation setup (parameters that trickled down to Person from Building)
        if "class" in self.dest_floors_by_state_name.keys():
            if not self.home_floor in self.dest_floors_by_state_name["class"]:
                self.dest_floors_by_state_name["class"].append(self.home_floor) # If we want some classes to be done virtually at home
        if "sleep" in self.dest_floors_by_state_name.keys():
            if not self.home_floor in self.dest_floors_by_state_name["sleep"]:
                self.dest_floors_by_state_name["sleep"].append(self.home_floor) # Sleep occurs at home
        if "meal" in self.dest_floors_by_state_name.keys():
            if not self.home_floor in self.dest_floors_by_state_name["meal"]:
                self.dest_floors_by_state_name["meal"].append(self.home_floor) # Meals can occur at home
        if "exercise" in self.dest_floors_by_state_name.keys():
            if not self.home_floor in self.dest_floors_by_state_name["exercise"]:
                self.dest_floors_by_state_name["exercise"].append(self.home_floor) # If we want some exercises to be done at home
        if "chores" in self.dest_floors_by_state_name.keys():
            if not self.home_floor in self.dest_floors_by_state_name["chores"]:
                self.dest_floors_by_state_name["chores"].append(self.home_floor) # Chores occur at home
        if "study" in self.dest_floors_by_state_name.keys():
            if not self.home_floor in self.dest_floors_by_state_name["study"]:
                self.dest_floors_by_state_name["study"].append(self.home_floor) # If we want some studying to be done at home

