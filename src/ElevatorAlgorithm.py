import numpy as np

class ElevatorAlgorithm:
    algorithm = ""

    """
    Takes:
    algorithm - String representing the algorithm to use.
    """
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def assign_stop(self, elevators, requested_floor, direction):
        if self.algorithm == "stay_where_stopped":
            assign_stop_SWS(elevators, requested_floor, direction)
        else:
            assign_stop_RTG(elevators, requested_floor, direction)


"""
stay_where_stopped algorithm (SWS):

When an elevator visits the last floor on its stop list, it remains idle on that floor until it is assigned a new stop.

A floor with a requested stop will be assigned to the nearest elevator currently moving towards this floor, unless there is an idle elevator already on the correct floor.

If there are no elevators moving towards the floor of the requested stop, the nearest idle elevator is assigned the stop.

# One of these two is used, not both. Further research is needed to determine what HERE uses.
If there are no idle elevators, the requested stop is assigned to the elevator with the shortest stop list.
If there are no idle elevators, the requested stop is assigned to the elevator who's last stop in it's stop list is closest to the floor of the requested stop.
"""

"""
Assigns a requested stop to one of the Elevators. (stay_where_stopped algorithm)

Takes:
elevators - List of Elevator classes
floor_id - Integer id of the floor an elevator needs to stop at
direction - String representing direction of travel, "up" or "down"

Returns:
assigned - Boolean representing if the requested stop was successfully assigned.
"""
def assign_stop_SWS(elevators, floor_id, direction):
    # Check if there is and Elevator that was previously scheduled to stop at the requested Floor
    for elevator in elevators:
        if direction == "up":
            if floor_id in elevator.up_stops:
                return True
        else:
            if floor_id in elevator.down_stops:
                return True

    # Check if there is an idle elevator on the correct floor
    for i in range(len(elevators)):
        if not elevators[i].is_moving and elevators[i].cur_floor == floor_id:
            if direction == "up":
                elevators[i].up_stops.append(floor_id)
                # Need to change state of Elevator here in case multiple stops need to be assigned during one simulation tick
                elevators[i].is_moving = True
                elevators[i].is_moving_up = True
            else:
                elevators[i].down_stops.append(floor_id)
                # Need to change state of Elevator here in case multiple stops need to be assigned during one simulation tick
                elevators[i].is_moving = True
                elevators[i].is_moving_up = False
            return True
    # Sort Elevators into elevators_moving_towards and elevators_idle
    elevators_moving_towards = []
    elevators_idle = []
    for i in range(len(elevators)):
        if elevators[i].is_moving:
            if direction == "up":
                # Check if Elevator is moving up towards floor_id
                if elevators[i].cur_floor < floor_id and elevators[i].is_moving_up:
                    elevators_moving_towards.append(elevators[i])
            else:
                # Check if Elevator is moving down towards floor_id
                if elevators[i].cur_floor > floor_id and not elevators[i].is_moving_up:
                    elevators_moving_towards.append(elevators[i])
            
        else:
            elevators_idle.append(elevators[i])
    # Assign the nearest elevator moving towards, if one exists
    if len(elevators_moving_towards) != 0:
        min_dist = np.inf
        min_idx = 0
        for i in range(len(elevators_moving_towards)):
            dist = np.abs(floor_id - elevators_moving_towards[i].cur_floor)
            if dist < min_dist:
                min_dist = dist
                min_idx = i
        if direction == "up":
            elevators_moving_towards[min_idx].up_stops.append(floor_id)
        else:
            elevators_moving_towards[min_idx].down_stops.append(floor_id)

    # If there are no elevators moving towards, assign nearest idle elevator, if one exists
    elif len(elevators_idle) != 0:
        min_dist = np.inf
        min_idx = 0
        for i in range(len(elevators_idle)):
            dist = np.abs(floor_id - elevators_idle[i].cur_floor)
            if dist < min_dist:
                min_dist = dist
                min_idx = i

        if elevators_idle[min_idx].cur_floor < floor_id:
            elevators_idle[min_idx].up_stops.append(floor_id)
            # Need to change state of Elevator here in case multiple stops need to be assigned during one simulation tick
            elevators_idle[min_idx].is_moving = True
            elevators_idle[min_idx].is_moving_up = True
        else:
            elevators_idle[min_idx].down_stops.append(floor_id)
            # Need to change state of Elevator here in case multiple stops need to be assigned during one simulation tick
            elevators_idle[min_idx].is_moving = True
            elevators_idle[min_idx].is_moving_up = False
        #if direction == "up":
            
        #else:
            
    
    # If there are no elevators moving towards and no idle elevators, this stop is not assigned yet. It will be assigned at a later simulation step when one of those two conditions are met.
    else:
        return False

    return True

"""
Assigns a requested stop to one of the Elevators. (return_to_ground algorithm)

Takes:
elevators - List of Elevator classes
floor_id - Integer id of the floor an elevator needs to stop at
direction - String representing direction of travel, "up" or "down"
"""
def assign_stop_RTG(elevators, floor_id, direction):
    return