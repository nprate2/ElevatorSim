from copy import deepcopy
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from Building import Building
from Floor import Floor
from Person import Person
from Elevator import Elevator
import Simulation
from Analytics import Analytics

state_names = ["freetime", "class", "sleep", "meal", "exercise", "shop", "chores", "study"]

HERE_floor_populations = [0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
HERE_dest_floors_by_state_name = {
    "freetime": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], # Person can go anywhere during freetime
    "class": [0], # Must go to ground floor for in person class
    "sleep": [], # Sleep only happens at person's home floor
    "meal": [0], # Must go to ground floor to eat out / pickup food
    "exercise": [1], # HERE gym is on second floor
    "shop": [0], # Must go to ground floor to go to store
    "chores": [], # Chores only happen at person's home floor
    "study": [3], # HERE study rooms are on fourth floor
}
HERE_elevator_algorithm = "stay_where_stopped"
HERE_elevator_starting_floors = [0, 0, 0]
HERE_elevator_capacities = [10, 10, 10]
#HERE_elevator_steps_per_stops = [5, 5, 5] # Num simulation steps an elevator must pass (doing nothing) each time it stops to onload or offload passengers
HERE_elevator_steps_per_stops = [1, 1, 1] # Num simulation steps an elevator must pass (doing nothing) each time it stops to onload or offload passengers

building = Building(HERE_floor_populations, HERE_dest_floors_by_state_name, HERE_elevator_algorithm, HERE_elevator_starting_floors, HERE_elevator_capacities, HERE_elevator_steps_per_stops)

"""
people = []
for i in tqdm(range(1000)):
    people.append(Person(i, i%15, 0.25, 2, HERE_dest_floors_by_state_name))

for i in range(1000):
    if np.array_equal(people[i].state_change_steps, people[i-1].state_change_steps):
        print("Uh Oh")
    #print(people[i].state_change_steps[0])
    #print(people[i].state_change_ids[0])
"""
analytics = Analytics()
# 1 step = 3.5 seconds. 86,400 seconds in a day. ~24,686 steps. 24,686 / 24 = 1,028.58 = ~1029 steps per hour
num_steps_per_day = 24686

for day in tqdm(range(7)):
    for step in tqdm(range(int(num_steps_per_day))):
        analytics.evaluate_simulation(building, day, step)

        Simulation.handle_state_changes(building, day, step) # First. Check if anybody not waiting for an elevator needs to start doing so.
        #building.print_building_state()
        Simulation.handle_new_button_presses(building)

        Simulation.update_elevators(building) # Update all Elevators, active and idle. (handles stopping to onboard, offload, switching from active to idle or visa versa, moving Persons from Elevators to Floors or visa versa, etc.)
        Simulation.update_counters(building, day) # Last. Update the counters of anybody waiting for an elevator or anybody traveling on an elevator.
analytics.compute_daily_step_averages(building)
analytics.compute_hourly_step_averages(building)

analytics.graph_daily_step_averages()
analytics.graph_hourly_step_averages()
analytics.graph_daily_minute_averages()
analytics.graph_hourly_minute_averages()
        