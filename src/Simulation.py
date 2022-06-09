from copy import deepcopy
import numpy as np

import Schedule

"""
This is the Simulation function heirarchy for the four core Simulation functionalities: handle_state_changes(), update_counters(), handle_new_button_presses(), and update_elevators().
Entries appear in the order they are located in this file.

        state_change_going_down(building, floor_id, person)
        state_change_going_up(building, floor_id, person)
    handle_state_change(building, day, person)
handle_state_changes(building, day, step)

update_counters(building, day)

    handle_new_up_button_presses(building)
    handle_new_down_button_presses(building)
handle_new_button_presses(building)

            handle_onboard(building, elevator)
            handle_offload(building, elevator)
        update_active_up_elevator(building, elevator)
        update_active_down_elevator(building, elevator)
    update_active_elevators(building, active_elevators)
    update_idle_elevators(building, idle_elevators)
update_elevators(building)
"""




"""
Updates a Building when a Person needs to travel down.

Takes:
buidling - Building class
floor_id - Integer representing the floor to be updated
person - Person class
"""
def state_change_going_down(building, floor_id, person):
    building.floors[floor_id].people_on_floor.remove(person)
    building.floors[floor_id].people_going_down.append(person)
    if not building.floors[floor_id].is_down_pressed:
        building.floors[floor_id].is_down_pressed = True
        building.floors_new_down_button.append(floor_id)
"""
Updates a Building when a Person needs to travel up.

Takes:
buidling - Building class
floor_id - Integer representing the floor to be updated
person - Person class
"""
def state_change_going_up(building, floor_id, person):
    building.floors[floor_id].people_on_floor.remove(person)
    building.floors[floor_id].people_going_up.append(person)
    if not building.floors[floor_id].is_up_pressed:
        building.floors[floor_id].is_up_pressed = True
        building.floors_new_up_button.append(floor_id)

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

    # Choose a destination floor based on the Person's dest_floors_by_state_name
    person.dest_floor = np.random.choice(person.dest_floors_by_state_name[Schedule.state_name_by_id[new_state]])

    # Determine if the Person needs to travel up or down
    cur_floor_id = person.cur_floor
    if person.dest_floor == cur_floor_id:
        return # Person is already on the floor they want to travel to
    elif person.dest_floor < cur_floor_id:
        state_change_going_down(building, cur_floor_id, person)
    else:
        state_change_going_up(building, cur_floor_id, person)

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
            if len(person.state_change_steps[day]) != 0: # Check that there are state changes left (they are popped within handle_state_change)
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

    # Update Person traveling counters, Elevator idle counters, Elevator stopped counters, and Elevator active counters
    for i in range(len(building.elevators)):
        # Person traveling counters
        for key in building.elevators[i].people_by_destination.keys():
            people = building.elevators[i].people_by_destination[key]
            for j in range(len(people)):
                people[j].steps_traveling[day] += 1

        # Elevator idle, stopped, and active counters
        if building.elevators[i].is_moving:
            #print("update active")
            if building.elevators[i].stopped_steps != 0:
                building.elevators[i].steps_stopped[day] += 1
            else:
                building.elevators[i].steps_active[day] += 1
        else:
            #print("update idle")
            building.elevators[i].steps_idle[day] += 1

"""
Assigns all Floors within the Building's "floors_new_up_button" list to one of the Building's Elevators. Utilizes the ElevatorAlgorithm of the Building.

Takes:
building - Building class
"""            
def handle_new_up_button_presses(building):
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

"""
Assigns all Floors within the Building's "floors_new_down_button" list to one of the Building's Elevators. Utilizes the ElevatorAlgorithm of the Building.

Takes:
building - Building class
"""
def handle_new_down_button_presses(building):
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
Assigns all Floors within the Building's "floors_new_up_button" and "floors_new_down_button" lists to one of the Building's Elevators.

Takes:
building - Building class
"""
def handle_new_button_presses(building):
    handle_new_up_button_presses(building)
    handle_new_down_button_presses(building)
    
"""
Handles Persons onboarding an Elevator to go up at its current floor.

Takes:
building - Building class
elevator - Elevator class that is active and onboarding Persons to go up
"""
def handle_onboard_up(building, elevator):
    people_onboarding = building.floors[elevator.cur_floor].people_going_up
    for person in people_onboarding:
        # Remove each onboarding person from the people_going_up list on this floor
        building.floors[elevator.cur_floor].people_going_up.remove(person)

        # Add Person to the list associated with their destination floor
        if person.dest_floor in elevator.people_by_destination.keys():
            elevator.people_by_destination[person.dest_floor].append(person)
        else:
            elevator.people_by_destination[person.dest_floor] = deepcopy([person])
        
        # If their destination floor is not yet in the Elevator's stop list, add it
        if person.dest_floor not in elevator.up_stops:
            elevator.up_stops.append(person.dest_floor)
    # Reset the Floor's up button
    if building.floors[elevator.cur_floor].is_up_pressed:
        building.floors[elevator.cur_floor].is_up_pressed = False
"""
Handles Persons onboarding an Elevator to go down at its current floor.

Takes:
building - Building class
elevator - Elevator class that is active and onboarding Persons to go down
"""
def handle_onboard_down(building, elevator):
    people_onboarding = building.floors[elevator.cur_floor].people_going_down
    for person in people_onboarding:
        # Remove each onboarding person from the people_going_down list on this floor
        building.floors[elevator.cur_floor].people_going_down.remove(person)
        
        # Add Person to the list associated with their destination floor
        if person.dest_floor in elevator.people_by_destination.keys():
            elevator.people_by_destination[person.dest_floor].append(person)
        else:
            elevator.people_by_destination[person.dest_floor] = deepcopy([person])
        
        # If their destination floor is not yet in the Elevator's stop list, add it
        if person.dest_floor not in elevator.down_stops:
            elevator.down_stops.append(person.dest_floor)

    # Reset the Floor's down button
    if building.floors[elevator.cur_floor].is_down_pressed:
        building.floors[elevator.cur_floor].is_down_pressed = False

"""
Handles people onboarding an Elevator at its current floor.

Takes:
building - Building class
elevator - Elevator class that is active
"""
def handle_onboard(building, elevator):
    # Check if this is a deidled stop (the stop that caused an Elevator to switch from idle to active)
    if elevator.deidled_floor != -1:
        if elevator.deidled_floor_direction == "up":
            # Elevator is picking up Persons that want to go up, regardless of the Elevator's direction of travel
            handle_onboard_up(building, elevator)
        else:
            # Elevator is picking up Persons that want to go down, regardless of the Elevator's direction of travel
            handle_onboard_down(building, elevator)

    # If it isn't a deidled stop, determine if the Elevator is moving up or down
    elif elevator.is_moving_up:
        handle_onboard_up(building, elevator)

    else:
        handle_onboard_down(building, elevator)

"""
Handles people offloading an Elevator at its current floor.

Takes:
building - Building class
elevator - Elevator class that is active
"""
def handle_offload(building, elevator):
    people_offloading = elevator.people_by_destination[elevator.cur_floor]
    if len(people_offloading) != 0:
        for person in people_offloading:
            # Update Person's cur_floor, the Floor's people_on_floor, and the Elevator's people_by_destination
            person.cur_floor = elevator.cur_floor
            building.floors[elevator.cur_floor].people_on_floor.append(person)
            elevator.people_by_destination[elevator.cur_floor].remove(person)


"""
Updates an active Elevator travelling up in a Building each tick of simulation.

Takes:
building - Building class
elevator - Elevator class that is active and traveling up
"""
def update_active_up_elevator(building, elevator):
    if elevator.cur_floor < 0:
        print("update active up sub zero")
        exit()
    if elevator.cur_floor >= len(building.floors):
        print("update active up too large")
        exit()
    # Check if elevator has stopped_steps remaining (it is in the process of onloading or offloading Persons)
    if elevator.stopped_steps != 0:
        elevator.stopped_steps -= 1

        if elevator.stopped_steps == 0:
            # If this was the last step to spend onboarding/offloading, then we check if the elevator has more stops or if it should become idle
            if len(elevator.up_stops) == 0:
                if len(elevator.down_stops) == 0:
                    # Then this Elevator becomes idle
                    #print("set elev " + str(elevator.id) + " idle")
                    elevator.is_moving = False
                else:
                    # Then this Elevator switches direction of travel (from up to down)
                    elevator.is_moving_up = False
            else:
                # More up stops
                elevator.cur_floor += 1 # Increment the cur_floor to signify moving up a floor
        return # If stopped, the elevator does nothing.
    
    if elevator.cur_floor in elevator.up_stops:
        elevator.stopped_steps = elevator.steps_per_stop # If Elevator is stopping to onboard or offload Persons, set stopped_steps counter

        # Handle people that want to onboard
        handle_onboard(building, elevator)
        
        # Handle people that want to offload
        handle_offload(building, elevator)

        # Remove the handled floor from up_stops
        elevator.up_stops.remove(elevator.cur_floor)

        # If the elevator had deidled_floor set, it just got handled and should be set back to -1 to signify it is ready to recieve more stops.
        if elevator.deidled_floor != -1:
            elevator.deidled_floor = -1
    
    else:
        elevator.cur_floor += 1 # Increment the cur_floor to signify moving up a floor
        
    return

"""
Updates an active Elevator travelling down in a Building each tick of simulation.

Takes:
building - Building class
elevator - Elevator class that is active and traveling down
"""
def update_active_down_elevator(building, elevator):
    if elevator.cur_floor < 0:
        print("update active down sub zero")
        exit()
    if elevator.cur_floor >= len(building.floors):
        print("update active down too large")
        exit()
    # Check if elevator has stopped_steps remaining (it is in the process of onloading or offloading Persons)
    if elevator.stopped_steps != 0:
        elevator.stopped_steps -= 1

        if elevator.stopped_steps == 0:
            # If this was the last step to spend onboarding/offloading, then we check if the elevator has more stops or if it should become idle
            if len(elevator.down_stops) == 0:
                if len(elevator.up_stops) == 0:
                    # Then this Elevator becomes idle
                    #print("set elev " + str(elevator.id) + " idle")
                    elevator.is_moving = False
                else:
                    # Then this Elevator switches direction of travel (from down to up)
                    elevator.is_moving_up = True
            else:
                # More down stops
                elevator.cur_floor -= 1 # Decrement the cur_floor to signify the Elevator moving down a floor
        return # If stopped, the elevator does nothing.

    if elevator.cur_floor in elevator.down_stops:
        elevator.stopped_steps = elevator.steps_per_stop # If Elevator is stopping to onboard Persons, set stopped_steps counter

        # Handle people that want to onboard
        handle_onboard(building, elevator)
    
        # Handle people that want to offload
        handle_offload(building, elevator)

        # Remove the handled floor from down_stops
        elevator.down_stops.remove(elevator.cur_floor)

        # If the elevator had deidled_floor set, it just got handled and should be set back to -1 to signify it is ready to recieve more stops.
        if elevator.deidled_floor != -1:
            elevator.deidled_floor = -1
    else:
        elevator.cur_floor -= 1 # Decrement the cur_floor to signify the Elevator moving down a floor

    return

"""
Updates all active Elevators in a Building each tick of simulation.

Takes:
building - Building 
active_elevators - list of Elevators that are active
"""
def update_active_elevators(building, active_elevators):
    for i in range(len(active_elevators)):

        if active_elevators[i].is_moving_up: # Elevator moving up
            update_active_up_elevator(building, active_elevators[i])
            
        else: # Elevator moving down
            update_active_down_elevator(building, active_elevators[i])




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
            print("set elev " + str(idle_elevator.id) + " active going up")
            idle_elevator.is_moving = True
            idle_elevator.is_moving_up = True

        elif len(idle_elevator.down_stops) != 0:
            # Set Elevator to active doing down
            print("set elev " + str(idle_elevator.id) + " active going down")
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
