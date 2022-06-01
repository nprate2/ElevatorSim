import numpy as np

import Schedule


"""
Handles a scheduled state change for a Person.
This function is called by update_people when a state change is detected,
thus the next state change within the Person's schedule is the one to handle (this is the 0th index always because handled data is pop()ed).

Takes:
buidling - Building class
day - integer representing day of the week (0-6 where 0 corresponds to Sunday and 6 corresponds to Saturday)
person - Person class
"""
def handle_state_change(building, day, person):
    # Grab the next state and remove old data
    new_state = person.state_change_ids[day][0, 1]
    person.state_change_ids[day] = person.state_change_ids[day][1:]
    person.state_change_steps[day] = person.state_change_steps[day][1:]

    person.dest_floor = np.random.choice(person.dest_floors_by_state_name[Schedule.state_name_by_id[new_state]])
    cur_floor = person.cur_floor
    cur_floor_idx = cur_floor - 1 # Since building.floors is 0 indexed while floor ids are 1 indexed
    if person.dest_floor == cur_floor:
        return # Person is already on the floor they want to travel to
    elif person.dest_floor < cur_floor:
        # Person needs to go down
        building.floors[cur_floor_idx].people_on_floor.remove(person)
        building.floors[cur_floor_idx].people_going_down.append(person)
        if not building.floors[cur_floor_idx].is_down_pressed:
            building.floors[cur_floor_idx].is_down_pressed = True
            building.floors_new_down_button.append(cur_floor)
    else:
        # Person needs to go up
        building.floors[cur_floor_idx].people_on_floor.remove(person)
        building.floors[cur_floor_idx].people_going_up.append(person)
        if not building.floors[cur_floor_idx].is_up_pressed:
            building.floors[cur_floor_idx].is_up_pressed = True
            building.floors_new_up_button.append(cur_floor)

"""
Checks for and handles scheduled state changes for all Person classes in a Building class

Takes:
building - Building class
day - integer representing day of the week (0-6 where 0 corresponds to Sunday and 6 corresponds to Saturday)
step - integer representing the step number of the simulation on the given day

"""
def handle_state_changes(building, day, step):
    for i in range(len(building.floors)):
        people = building.floors[i].people_on_floor
        for person in people:
            if person.state_change_steps[day][0] == step:
                handle_state_change(building, day, person)

"""
Updates the steps_waiting and steps_traveling counters within the Person class

Takes:
building - Building class
day - integer representing day of the week (0-6 where 0 corresponds to Sunday and 6 corresponds to Saturday)
"""
def update_counters(building, day):
    for i in range(len(building.floors)):
        # Update Person waiting counters
        people_going_up = building.floors[i].people_going_up
        people_going_down = building.floors[i].people_going_down

        for person in people_going_up:
            person.steps_waiting[day] += 1
        for person in people_going_down:
            person.steps_waiting[day] += 1

    # Update Person traveling counters, Elevator idle counters, and Elevator active counters
    for i in range(len(building.elevators)):
        # Person traveling counters
        for key in building.elevators[i].people_by_destination.keys():
            people = building.elevators[i].people_by_destination[key]
            for j in range(len(people)):
                people[j].steps_traveling[day] += 1

        # Elevator idle and active counters
        if building.elevators[i].is_moving:
            #print("update active")
            building.elevators[i].steps_active[day] += 1
        else:
            #print("update idle")
            building.elevators[i].steps_idle[day] += 1
            

"""
Assigns all Floors within the Building's "floors_new_up_button" and "floors_new_down_button" lists to one of the Building's Elevators. Utilizes the ElevatorAlgorithm of the Building.

Takes:
building - Building class
"""
def handle_new_button_presses(building):
    idxs_to_pop = [] # Used to track which up stop idxs have been assigned
    for i in range(len(building.floors_new_up_button)):
        requested_floor = building.floors_new_up_button[i]
        assigned = building.elevator_algorithm.assign_stop(building.elevators, requested_floor, "up") # Attempt to assign stop
        if assigned:
            idxs_to_pop.append(i)
    idxs_to_pop.reverse() # So we pop largest idxs first (popping smallest idxs would mess up larger idxs)
    # Pop assigned up stops
    for idx in idxs_to_pop:
        building.floors_new_up_button.pop(idx)

    idxs_to_pop = [] # Used to track which down stop idxs have been assigned
    for i in range(len(building.floors_new_down_button)):
        requested_floor = building.floors_new_down_button[i]
        assigned = building.elevator_algorithm.assign_stop(building.elevators, requested_floor, "down") # Attempt to assign stop
        if assigned:
            idxs_to_pop.append(i)
    idxs_to_pop.reverse() # So we pop largest idxs first (popping smallest idxs would mess up larger idxs)
    # Pop assigned down stops
    for idx in idxs_to_pop:
        building.floors_new_down_button.pop(idx)

"""
Updates all active Elevators in a Building each tick of simulation.

Takes:
building - Building class
"""
def update_active_elevators(building, active_elevators):
    for i in range(len(active_elevators)):
        active_elevator = active_elevators[i]
        # Check if elevator has stopped_steps remaining (it is in the process of onloading or offloading Persons)
        if active_elevator.stopped_steps != 0:
            active_elevator.stopped_steps -= 1
            continue # If stopped, the elevator does nothing.

        new_floor = 0
        # Update Elevator's current floor, stop lists, and motion / state
        if active_elevator.is_moving_up: # Elevator moving up
            new_floor = active_elevator.cur_floor + 1
            if new_floor in active_elevator.up_stops:
                active_elevator.stopped_steps = active_elevator.steps_per_stop # If Elevator is stopping to onboard Persons, set stopped_steps counter
                people_onboarding = building.floors[new_floor-1].people_going_up
                for person in people_onboarding:
                    building.floors[new_floor-1].people_going_up.remove(person)
                    active_elevator.people_by_destination[person.dest_floor].append(person) # Add Person to the list associated with their destination floor
                    if person.dest_floor not in active_elevator.up_stops: # If their destination floor is not yet in the Elevator's stop list, add it
                        active_elevator.up_stops.append(person.dest_floor)


                active_elevator.up_stops.remove(new_floor)
                if len(active_elevator.up_stops) == 0:
                    if len(active_elevator.down_stops) == 0:
                        # Then this Elevator becomes idle
                        active_elevator.is_moving = False
                    else:
                        # Then this Elevator switches direction of travel (from up to down)
                        active_elevator.is_moving_up = False
            
        else: # Elevator moving down
            new_floor = active_elevator.cur_floor - 1
            if new_floor in active_elevator.down_stops:
                active_elevator.stopped_steps = active_elevator.steps_per_stop # If Elevator is stopping to onboard Persons, set stopped_steps counter
                people_onboarding = building.floors[new_floor-1].people_going_down
                for person in people_onboarding:
                    building.floors[new_floor-1].people_going_down.remove(person)
                    active_elevator.people_by_destination[person.dest_floor].append(person) # Add Person to the list associated with their destination floor
                    if person.dest_floor not in active_elevator.down_stops: # If their destination floor is not yet in the Elevator's stop list, add it
                        active_elevator.up_stops.append(person.dest_floor)


                active_elevator.down_stops.remove(new_floor)
                if len(active_elevator.down_stops) == 0:
                    if len(active_elevator.up_stops) == 0:
                        # Then this Elevator becomes idle
                        active_elevator.is_moving = False
                    else:
                        # Then this Elevator switches direction of travel (from down to up)
                        active_elevator.is_moving_up = True

        active_elevator.cur_floor  = new_floor

        # Check if people want to get off at this new_floor
        people_offloading = active_elevator.people_by_destination[new_floor]
        if len(people_offloading) != 0:
            # If Elevator is stopping to offload people, set its stopped_steps counter
            active_elevator.stopped_steps = active_elevator.steps_per_stop
            # Handle the people offloading
            for person in people_offloading:
                building.floors[new_floor].people_on_floor.append(person)
            active_elevator.people_by_destination.pop(new_floor)




"""
Updates all idle Elevators in a Building each tick of simulation.

Takes:
building - Building class
"""
def update_idle_elevators(building, idle_elevators):
    for i in range(len(idle_elevators)):
        idle_elevator = idle_elevators[i]
        if len(idle_elevator.up_stops) != 0:
            # Set Elevator to active going up
            idle_elevator.is_moving = True
            idle_elevator.is_moving_up = True

        elif len(idle_elevator.down_stops) != 0:
            # Set Elevator to active doing down
            idle_elevator.is_moving = True
            idle_elevator.is_moving_up = False


"""
Updates all Elevators in a Building each tick of simulation utilizing the two elevator update functions defined above.

Takes:
building - Building class
"""
def update_elevators(building):
    active_elevators = []
    idle_elevators = []
    # Find active and idle elevators
    for i in range(len(building.elevators)):
        if building.elevators[i].is_moving:
            active_elevators.append(building.elevators[i])
        else:
            idle_elevators.append(building.elevators[i])
    # Update active and idle elevators
    update_active_elevators(building, active_elevators)
    update_idle_elevators(building, idle_elevators)
