from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

import constants

class Analytics:
    cur_day = 0

    daily_avg_elevator_idle_steps = []
    daily_avg_elevator_active_steps = []
    daily_avg_elevator_loading_steps = []
    daily_avg_elevator_returning_steps = []

    daily_avg_person_riding_steps = []
    daily_avg_person_waiting_steps = []

    hourly_avg_elevator_idle_steps = []
    hourly_avg_elevator_active_steps = []
    hourly_avg_elevator_loading_steps = []
    hourly_avg_elevator_returning_steps = []

    hourly_avg_person_riding_steps = []
    hourly_avg_person_waiting_steps = []
    
    """
    Ensures all class lists use unique memory for each Analytics instance
    """
    def __init__(self):
        self.daily_avg_elevator_idle_steps = deepcopy(self.daily_avg_elevator_idle_steps)
        self.daily_avg_elevator_active_steps = deepcopy(self.daily_avg_elevator_active_steps)
        self.daily_avg_elevator_loading_steps = deepcopy(self.daily_avg_elevator_loading_steps)
        self.daily_avg_elevator_returning_steps = deepcopy(self.daily_avg_elevator_returning_steps)

        self.daily_avg_person_riding_steps = deepcopy(self.daily_avg_person_riding_steps)
        self.daily_avg_person_waiting_steps = deepcopy(self.daily_avg_person_waiting_steps)

        self.hourly_avg_elevator_idle_steps = deepcopy(self.hourly_avg_elevator_idle_steps)
        self.hourly_avg_elevator_active_steps = deepcopy(self.hourly_avg_elevator_active_steps)
        self.hourly_avg_elevator_loading_steps = deepcopy(self.hourly_avg_elevator_loading_steps)
        self.hourly_avg_elevator_returning_steps = deepcopy(self.hourly_avg_elevator_returning_steps)

        self.hourly_avg_person_riding_steps = deepcopy(self.hourly_avg_person_riding_steps)
        self.hourly_avg_person_waiting_steps = deepcopy(self.hourly_avg_person_waiting_steps)

    """
    Converts simulation steps to seconds

    Takes:
    steps - integer representing a number of simulation steps
    """
    def steps_to_seconds(self, steps):
        return steps * constants.seconds_per_step

    """
    Converts simulation steps to minues
    
    Takes:
    steps - integer representing a number of simulation steps
    """
    def steps_to_minutes(self, steps):
        return (steps * constants.seconds_per_step) / 60

    """
    Converts simulation steps to hours

    Takes:
    steps - integer representing a number of simulation steps
    """
    def steps_to_hours(self, steps):
        return ((steps * constants.seconds_per_step) / 60) / 60

    """
    Converts simulation steps to days

    Takes:
    steps - integer representing a number of simulation steps
    """
    def steps_to_days(self, steps):
        return (((steps * constants.seconds_per_step) / 60) / 60) / 24
    
    """
    Adds a Person's daily counters to the running sums to be averaged in the future, and reset counters to zero.
    A Person's counters list is structured as so:
    0 - daily steps waiting, 1 - hourly steps waiting, 2 - daily steps riding, 3 - hourly steps riding

    Takes:
    person - Person class
    """
    def handle_daily_person_counters(self, person):
        self.daily_avg_person_waiting_steps[-1] += person.waiting_counters[0]
        self.daily_avg_person_riding_steps[-1] += person.riding_counters[0]

        person.waiting_counters[0] = 0
        person.riding_counters[0] = 0

        #self.daily_avg_person_waiting_steps[-1] += person.daily_steps_waiting
        #self.daily_avg_person_riding_steps[-1] += person.daily_steps_riding
        #person.daily_steps_waiting = 0
        #person.daily_steps_riding = 0

    """
    Adds a Person's hourly counters to the running sums to be averaged in the future, and reset counters to zero.
    A Person's counters list is structured as so:
    0 - daily steps waiting, 1 - hourly steps waiting, 2 - daily steps riding, 3 - hourly steps riding

    Takes:
    person - Person class
    """
    def handle_hourly_person_counters(self, person):
        self.hourly_avg_person_waiting_steps[-1] += person.waiting_counters[1]
        self.hourly_avg_person_riding_steps[-1] += person.riding_counters[1]

        person.waiting_counters[1] = 0
        person.riding_counters[1] = 0

        #self.hourly_avg_person_waiting_steps[-1] += person.hourly_steps_waiting
        #self.hourly_avg_person_riding_steps[-1] += person.hourly_steps_riding
        #person.hourly_steps_waiting = 0
        #person.hourly_steps_riding = 0
    
    """
    Adds an Elevator's daily counters to the running sums to be averaged in the future, and reset counters to zero.
    An Elevator's counters list is structured as so:
    0 - daily steps idle, 1 - hourly steps idle, 2 - daily steps active,
    3 - hourly steps active, 4 - daily steps loading, 5 - hourly steps loading

    Takes:
    elevator - Elevator class
    """
    def handle_daily_elevator_counters(self, elevator):
        self.daily_avg_elevator_idle_steps[-1] += elevator.idle_counters[0]
        self.daily_avg_elevator_active_steps[-1] += elevator.active_counters[0]
        self.daily_avg_elevator_loading_steps[-1] += elevator.loading_counters[0]
        self.daily_avg_elevator_returning_steps[-1] += elevator.returning_counters[0]

        elevator.idle_counters[0] = 0
        elevator.active_counters[0] = 0
        elevator.loading_counters[0] = 0
        elevator.returning_counters[0] = 0

        #self.daily_avg_elevator_active_steps[-1] += elevator.daily_steps_active
        #self.daily_avg_elevator_idle_steps[-1] += elevator.daily_steps_idle
        #self.daily_avg_elevator_loading_steps[-1] += elevator.daily_steps_loading
        #elevator.daily_steps_active = 0
        #elevator.daily_steps_idle = 0
        #elevator.daily_steps_loading = 0

    """
    Adds an Elevator's hourly counters to the running sums to be averaged in the future, and reset counters to zero.
    An Elevator's counters list is structured as so:
    0 - daily steps idle, 1 - hourly steps idle, 2 - daily steps active,
    3 - hourly steps active, 4 - daily steps loading, 5 - hourly steps loading

    Takes:
    elevator - Elevator class
    """
    def handle_hourly_elevator_counters(self, elevator):
        self.hourly_avg_elevator_idle_steps[-1] += elevator.idle_counters[1]
        self.hourly_avg_elevator_active_steps[-1] += elevator.active_counters[1]
        self.hourly_avg_elevator_loading_steps[-1] += elevator.loading_counters[1]
        self.hourly_avg_elevator_returning_steps[-1] += elevator.returning_counters[1]

        elevator.idle_counters[1] = 0
        elevator.active_counters[1] = 0
        elevator.loading_counters[1] = 0
        elevator.returning_counters[1] = 0

        #self.hourly_avg_elevator_active_steps[-1] += elevator.hourly_steps_active
        #self.hourly_avg_elevator_idle_steps[-1] += elevator.hourly_steps_idle
        #self.hourly_avg_elevator_loading_steps[-1] += elevator.hourly_steps_loading
        #elevator.hourly_steps_active = 0
        #elevator.hourly_steps_idle = 0
        #elevator.hourly_steps_loading = 0

    """
    Computes all daily step averages for today and append the value to this class's lists.
    This function is called by evaluate_simulation when a day change is detected.
    This function sets other class's daily counters to 0 such that they start tracking data for this new day.
    handle_daily_person_counters and handle_daily_elevator_counters sum values of counters which are then averaged at the end of this function.

    Takes:
    building - Building class
    """
    def compute_daily_step_averages(self, building):
        self.daily_avg_elevator_idle_steps.append(0.0)
        self.daily_avg_elevator_active_steps.append(0.0)
        self.daily_avg_elevator_loading_steps.append(0.0)
        self.daily_avg_elevator_returning_steps.append(0.0)

        self.daily_avg_person_riding_steps.append(0.0)
        self.daily_avg_person_waiting_steps.append(0.0)

        # Sum all Person daily counters and reset them to 0 for next day. Need to check people on floor, waiting to travel, and currently riding
        for floor in building.floors:
            # People on floor
            for person in floor.people_on_floor:
                self.handle_daily_person_counters(person)
            # People on floor going up
            for person in floor.people_going_up:
                self.handle_daily_person_counters(person)
            # People on floor going down
            for person in floor.people_going_down:
                self.handle_daily_person_counters(person)

        # Sum all Elevator daily counters and reset them to 0 for next day. Also handle the people that are riding.
        for elevator in building.elevators:
            # People riding on elevator
            for key in elevator.people_by_destination.keys():
                for person in elevator.people_by_destination[key]:
                    self.handle_daily_person_counters(person)

            self.handle_daily_elevator_counters(elevator)
        
        # Divide by totals to get average steps
        self.daily_avg_elevator_idle_steps[-1] /= len(building.elevators)
        self.daily_avg_elevator_active_steps[-1] /= len(building.elevators)
        self.daily_avg_elevator_loading_steps[-1] /= len(building.elevators)
        self.daily_avg_elevator_returning_steps[-1] /= len(building.elevators)

        self.daily_avg_person_riding_steps[-1] /= building.population
        self.daily_avg_person_waiting_steps[-1] /= building.population

    """
    Computes all hourly averages for today and append the value to this class's lists.
    This function is called by evaluate_simulation when an hour change is detected.
    This function sets other class's hourly counters to 0 such that they start tracking data for this new hour.
    handle_hourly_person_counters and handle_hourly_elevator_counters sum values of counters which are then averaged at the end of this function.

    Takes:
    building - Building class
    """
    def compute_hourly_step_averages(self, building):
        self.hourly_avg_elevator_idle_steps.append(0.0)
        self.hourly_avg_elevator_active_steps.append(0.0)
        self.hourly_avg_elevator_loading_steps.append(0.0)
        self.hourly_avg_elevator_returning_steps.append(0.0)

        self.hourly_avg_person_riding_steps.append(0.0)
        self.hourly_avg_person_waiting_steps.append(0.0)

        # Sum all Person waiting and riding hourly counters, and reset them to 0 for next day. Need to check people on floor, waiting to travel, and currently riding
        for floor in building.floors:
            # People on floor
            for person in floor.people_on_floor:
                self.handle_hourly_person_counters(person)

            # People going up on floor
            for person in floor.people_going_up:
                self.handle_hourly_person_counters(person)

            # People going down on floor
            for person in floor.people_going_down:
                self.handle_hourly_person_counters(person)

        # Sum all Elevator hourly counters and reset them to 0 for next day. Also handle the people that are riding.
        for elevator in building.elevators:
            # Sum all Person riding hourly counters on each Elevator, and reset them to 0 for next day
            for key in elevator.people_by_destination.keys():
                for person in elevator.people_by_destination[key]:
                    self.handle_hourly_person_counters(person)

            self.handle_hourly_elevator_counters(elevator)
        
        # Divide by totals to get average steps
        self.hourly_avg_elevator_idle_steps[-1] /= len(building.elevators)
        self.hourly_avg_elevator_active_steps[-1] /= len(building.elevators)
        self.hourly_avg_elevator_loading_steps[-1] /= len(building.elevators)
        self.hourly_avg_elevator_returning_steps[-1] /= len(building.elevators)

        self.hourly_avg_person_riding_steps[-1] /= building.population
        self.hourly_avg_person_waiting_steps[-1] /= building.population

    """
    Collects and manipulates data from a Building as a simulation runs.
    This function is called once for each simulation step.

    Takes:
    building - Building class
    day - integer representing the current day of the simulation
    step - integer representing the current step of the simulation within day
    """
    def evaluate_simulation(self, building, day, step):
        if self.cur_day != day:
            self.cur_day = day
            self.compute_daily_step_averages(building)

        if step % int(constants.steps_per_hour) == 0 and step != 0:
            self.compute_hourly_step_averages(building)
        return


    def print_defining_averages(self, building):
        #avg_daily_person_wait_time_seconds = self.steps_to_seconds(np.sum(self.daily_avg_person_waiting_steps) / len(constants.days_of_week))
        #avg_hourly_person_wait_time_seconds = self.steps_to_seconds(np.sum(self.hourly_avg_person_waiting_steps) / constants.hours_per_day)
        #print("Avg Hourly Person Wait Time (seconds):", avg_hourly_person_wait_time_seconds)
        avg_hourly_person_wait_time_minutes = self.steps_to_minutes(np.sum(self.hourly_avg_person_waiting_steps) / len(self.hourly_avg_person_waiting_steps))
        print("Avg Hourly Person Wait Time (minutes):", avg_hourly_person_wait_time_minutes)

        avg_daily_person_wait_time_hours = self.steps_to_hours(np.sum(self.daily_avg_person_waiting_steps) / len(self.daily_avg_person_waiting_steps))
        print("Avg Daily Person Wait Time (hours):", avg_daily_person_wait_time_hours)

















    """
    Graphs all daily step averages.
    """
    def graph_daily_step_averages(self):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
        fig.suptitle("Average Daily Elevator Steps Breakdown")

        ax1.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_idle_steps)
        ax1.set_ylim([0, int(constants.steps_per_day)])
        ax1.set_title("Steps Idle")

        ax2.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_active_steps)
        ax2.set_ylim([0, int(constants.steps_per_day)])
        ax2.set_title("Steps Active")

        ax3.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_loading_steps)
        ax3.set_ylim([0, int(constants.steps_per_day)])
        ax3.set_title("Steps Loading")

        ax4.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_returning_steps)
        ax4.set_ylim([0, int(constants.steps_per_day)])
        ax4.set_title("Steps Returning")

        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Average Daily Person Steps Breakdown')

        ax1.plot(constants.days_of_week_abbreviations, self.daily_avg_person_riding_steps)
        ax1.set_ylim([0, int(constants.steps_per_day)])
        ax1.set_title("Steps Riding")

        ax2.plot(constants.days_of_week_abbreviations, self.daily_avg_person_waiting_steps)
        ax2.set_ylim([0, int(constants.steps_per_day)])
        ax2.set_title("Steps Waiting")

        plt.show()
    
    """
    Graphs all hourly step averages.
    """
    def graph_hourly_step_averages(self):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
        fig.suptitle("Average Hourly Elevator Steps Breakdown")

        ax1.plot(self.hourly_avg_elevator_idle_steps)
        ax1.set_ylim([0, int(constants.steps_per_hour)])
        ax1.set_title("Steps Idle")

        ax2.plot(self.hourly_avg_elevator_active_steps)
        ax2.set_ylim([0, int(constants.steps_per_hour)])
        ax2.set_title("Steps Active")

        ax3.plot(self.hourly_avg_elevator_loading_steps)
        ax3.set_ylim([0, int(constants.steps_per_hour)])
        ax3.set_title("Steps loading")

        ax4.plot(self.hourly_avg_elevator_returning_steps)
        ax4.set_ylim([0, int(constants.steps_per_hour)])
        ax4.set_title("Steps Returning")

        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Average Hourly Person Steps Breakdown')

        ax1.plot(self.hourly_avg_person_riding_steps)
        ax1.set_ylim([0, int(constants.steps_per_hour)])
        ax1.set_title("Steps Riding")

        ax2.plot(self.hourly_avg_person_waiting_steps)
        ax2.set_ylim([0, int(constants.steps_per_hour)])
        ax2.set_title("Steps Waiting")

        plt.show()

    """
    Graphs all daily minute averages.
    """
    def graph_daily_minute_averages(self):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
        fig.suptitle("Average Daily Elevator Minutes Breakdown")

        ax1.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_idle_steps)))
        ax1.set_ylim([0, int(constants.minutes_per_day)])
        ax1.set_title("Minutes Idle")

        ax2.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_active_steps)))
        ax2.set_ylim([0, int(constants.minutes_per_day)])
        ax2.set_title("Minutes Active")

        ax3.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_loading_steps)))
        ax3.set_ylim([0, int(constants.minutes_per_day)])
        ax3.set_title("Minutes Loading")

        ax4.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_returning_steps)))
        ax4.set_ylim([0, int(constants.minutes_per_day)])
        ax4.set_title("Minutes Returning")

        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Average Daily Person Minutes Breakdown')

        ax1.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_person_riding_steps)))
        ax1.set_ylim([0, int(constants.minutes_per_day)])
        ax1.set_title("Minutes Riding")

        ax2.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_person_waiting_steps)))
        ax2.set_ylim([0, int(constants.minutes_per_day)])
        ax2.set_title("Minutes Waiting")

        plt.show()
    
    """
    Graphs all daily hourly averages.
    """
    def graph_hourly_minute_averages(self):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
        fig.suptitle("Average Hourly Elevator Minutes Breakdown")

        ax1.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_idle_steps)))
        ax2.set_ylim([0, int(constants.minutes_per_hour)])
        ax1.set_title("Minutes Idle")

        ax2.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_active_steps)))
        ax2.set_ylim([0, int(constants.minutes_per_hour)])
        ax2.set_title("Minutes Active")

        ax3.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_loading_steps)))
        ax3.set_ylim([0, int(constants.minutes_per_hour)])
        ax3.set_title("Minutes Loading")

        ax4.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_returning_steps)))
        ax4.set_ylim([0, int(constants.minutes_per_hour)])
        ax4.set_title("Minutes Returning")

        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Average Hourly Person Minutes Breakdown')

        ax1.plot(list(map(self.steps_to_minutes, self.hourly_avg_person_riding_steps)))
        ax1.set_ylim([0, int(constants.minutes_per_hour)])
        ax1.set_title("Minutes Riding")

        ax2.plot(list(map(self.steps_to_minutes, self.hourly_avg_person_waiting_steps)))
        ax2.set_ylim([0, int(constants.minutes_per_hour)])
        ax2.set_title("Minutes Waiting")

        plt.show()