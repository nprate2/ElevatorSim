from copy import deepcopy
import matplotlib.pyplot as plt

import constants

class Analytics:
    cur_day = 0

    daily_avg_elevator_idle_steps = []
    daily_avg_elevator_active_steps = []
    daily_avg_elevator_stopped_steps = []
    daily_avg_person_traveling_steps = []
    daily_avg_person_waiting_steps = []

    hourly_avg_elevator_idle_steps = []
    hourly_avg_elevator_active_steps = []
    hourly_avg_elevator_stopped_steps = []
    hourly_avg_person_traveling_steps = []
    hourly_avg_person_waiting_steps = []
    
    """
    Ensures all class lists use unique memory for each Analytics instance
    """
    def __init__(self):
        self.daily_avg_elevator_idle_steps = deepcopy(self.daily_avg_elevator_idle_steps)
        self.daily_avg_elevator_active_steps = deepcopy(self.daily_avg_elevator_active_steps)
        self.daily_avg_elevator_stopped_steps = deepcopy(self.daily_avg_elevator_stopped_steps)
        self.daily_avg_person_traveling_steps = deepcopy(self.daily_avg_person_traveling_steps)
        self.daily_avg_person_waiting_steps = deepcopy(self.daily_avg_person_waiting_steps)

        self.hourly_avg_elevator_idle_steps = deepcopy(self.hourly_avg_elevator_idle_steps)
        self.hourly_avg_elevator_active_steps = deepcopy(self.hourly_avg_elevator_active_steps)
        self.hourly_avg_elevator_stopped_steps = deepcopy(self.hourly_avg_elevator_stopped_steps)
        self.hourly_avg_person_traveling_steps = deepcopy(self.hourly_avg_person_traveling_steps)
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
    Computes all daily step averages for today and append the value to this class's lists.
    This function is called by evaluate_simulation when a day change is detected.
    This function sets other class's daily counters to 0 such that they start tracking data for this new day.

    Takes:
    building - Building class
    """
    def compute_daily_step_averages(self, building):
        self.daily_avg_elevator_idle_steps.append(0.0)
        self.daily_avg_elevator_active_steps.append(0.0)
        self.daily_avg_elevator_stopped_steps.append(0.0)
        self.daily_avg_person_traveling_steps.append(0.0)
        self.daily_avg_person_waiting_steps.append(0.0)

        # Sum all Person waiting daily counters on each Floor, and reset them to 0 for next day
        for i in range(len(building.floors)):
            for person in building.floors[i].people_going_up:
                self.daily_avg_person_waiting_steps[-1] += person.daily_steps_waiting
                person.daily_steps_waiting = 0

            for person in building.floors[i].people_going_down:
                self.daily_avg_person_waiting_steps[-1] += person.daily_steps_waiting
                person.daily_steps_waiting = 0
        
        for i in range(len(building.elevators)):
            # Sum all Person traveling daily counters on each Elevator, and reset them to 0 for next day
            for key in building.elevators[i].people_by_destination.keys():
                for person in building.elevators[i].people_by_destination[key]:
                    self.daily_avg_person_traveling_steps[-1] += person.daily_steps_traveling
                    person.daily_steps_traveling = 0

            # Sum all Elevator idle, active, stopped daily counters, and reset them to 0 for next day
            self.daily_avg_elevator_idle_steps[-1] += building.elevators[i].daily_steps_idle
            building.elevators[i].daily_steps_idle = 0
            self.daily_avg_elevator_active_steps[-1] += building.elevators[i].daily_steps_active
            building.elevators[i].daily_steps_active = 0
            self.daily_avg_elevator_stopped_steps[-1] += building.elevators[i].daily_steps_stopped
            building.elevators[i].daily_steps_stopped = 0
        
        # Divide by totals to get average steps
        self.daily_avg_elevator_idle_steps[-1] /= len(building.elevators)
        self.daily_avg_elevator_active_steps[-1] /= len(building.elevators)
        self.daily_avg_elevator_stopped_steps[-1] /= len(building.elevators)
        self.daily_avg_person_traveling_steps[-1] /= building.population
        self.daily_avg_person_waiting_steps[-1] /= building.population

    """
    Computes all hourly averages for today and append the value to this class's lists.
    This function is called by evaluate_simulation when a day change is detected.
    This function sets other class's hourly counters to 0 such that they start tracking data for this new day.

    Takes:
    building - Building class
    """
    def compute_hourly_step_averages(self, building):
        self.hourly_avg_elevator_idle_steps.append(0.0)
        self.hourly_avg_elevator_active_steps.append(0.0)
        self.hourly_avg_elevator_stopped_steps.append(0.0)
        self.hourly_avg_person_traveling_steps.append(0.0)
        self.hourly_avg_person_waiting_steps.append(0.0)

        # Sum all Person waiting hourly counters on each Floor, and reset them to 0 for next day
        for i in range(len(building.floors)):
            for person in building.floors[i].people_going_up:
                self.hourly_avg_person_waiting_steps[-1] += person.hourly_steps_waiting
                person.hourly_steps_waiting = 0

            for person in building.floors[i].people_going_down:
                self.hourly_avg_person_waiting_steps[-1] += person.hourly_steps_waiting
                person.hourly_steps_waiting = 0
        
        for i in range(len(building.elevators)):
            # Sum all Person traveling hourly counters on each Elevator, and reset them to 0 for next day
            for key in building.elevators[i].people_by_destination.keys():
                for person in building.elevators[i].people_by_destination[key]:
                    self.hourly_avg_person_traveling_steps[-1] += person.hourly_steps_traveling
                    person.hourly_steps_traveling = 0

            # Sum all Elevator idle, active, stopped hourly counters, and reset them to 0 for next day
            self.hourly_avg_elevator_idle_steps[-1] += building.elevators[i].hourly_steps_idle
            building.elevators[i].hourly_steps_idle = 0
            self.hourly_avg_elevator_active_steps[-1] += building.elevators[i].hourly_steps_active
            building.elevators[i].hourly_steps_active = 0
            self.hourly_avg_elevator_stopped_steps[-1] += building.elevators[i].hourly_steps_stopped
            building.elevators[i].hourly_steps_stopped = 0
        
        # Divide by totals to get average steps
        self.hourly_avg_elevator_idle_steps[-1] /= len(building.elevators)
        self.hourly_avg_elevator_active_steps[-1] /= len(building.elevators)
        self.hourly_avg_elevator_stopped_steps[-1] /= len(building.elevators)
        self.hourly_avg_person_traveling_steps[-1] /= building.population
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

        if (step + 1) % 1029 == 0:
            self.compute_hourly_step_averages(building)
        return

    """
    Graphs all daily step averages.
    """
    def graph_daily_step_averages(self):
        """
        #plot1 = plt.figure(1)
        plt.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_idle_steps)
        plt.title("Average Daily Elevator Steps Idle")
        
        #plot1 = plt.figure(2)
        plt.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_active_steps)
        plt.title("Average Daily Elevator Steps Active")
        
        #plot1 = plt.figure(3)
        plt.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_stopped_steps)
        plt.title("Average Daily Elevator Steps Stopped")
        """

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle("Average Daily Elevator Steps Breakdown")
        ax1.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_idle_steps)
        ax1.set_title("Steps Idle")
        ax2.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_active_steps)
        ax2.set_title("Steps Active")
        ax3.plot(constants.days_of_week_abbreviations, self.daily_avg_elevator_stopped_steps)
        ax3.set_title("Steps Stopped")

        plt.show()
        
        """
        #plot1 = plt.figure(4)
        plt.plot(constants.days_of_week_abbreviations, self.daily_avg_person_traveling_steps)
        plt.title("Average Daily Person Steps Traveling")
        
        #plot1 = plt.figure(5)
        plt.plot(constants.days_of_week_abbreviations, self.daily_avg_person_waiting_steps)
        plt.title("Average Daily Person Steps Waiting")

        plt.show()
        """

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Average Daily Person Steps Breakdown')
        ax1.plot(constants.days_of_week_abbreviations, self.daily_avg_person_traveling_steps)
        ax1.set_title("Steps Traveling")
        ax2.plot(constants.days_of_week_abbreviations, self.daily_avg_person_waiting_steps)
        ax2.set_title("Steps Waiting")

        plt.show()
    
    """
    Graphs all hourly step averages.
    """
    def graph_hourly_step_averages(self):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle("Average Hourly Elevator Steps Breakdown")
        ax1.plot(self.hourly_avg_elevator_idle_steps)
        ax1.set_title("Steps Idle")
        ax2.plot(self.hourly_avg_elevator_active_steps)
        ax2.set_title("Steps Active")
        ax3.plot(self.hourly_avg_elevator_stopped_steps)
        ax3.set_title("Steps Stopped")

        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Average Hourly Person Steps Breakdown')
        ax1.plot(self.hourly_avg_person_traveling_steps)
        ax1.set_title("Steps Traveling")
        ax2.plot(self.hourly_avg_person_waiting_steps)
        ax2.set_title("Steps Waiting")

        plt.show()


        """
        plt.plot(self.hourly_avg_elevator_idle_steps)
        plt.title("Average Hourly Elevator Steps Idle")
        plt.show()

        plt.plot(self.hourly_avg_elevator_active_steps)
        plt.title("Average Hourly Elevator Steps Active")
        plt.show()

        plt.plot(self.hourly_avg_elevator_stopped_steps)
        plt.title("Average Hourly Elevator Steps Stopped")
        plt.show()

        plt.plot(self.hourly_avg_person_traveling_steps)
        plt.title("Average Hourly Person Steps Traveling")
        plt.show()

        plt.plot(self.hourly_avg_person_waiting_steps)
        plt.title("Average Hourly Person Steps Waiting")
        plt.show()"""

    """
    Graphs all daily minute averages.
    """
    def graph_daily_minute_averages(self):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle("Average Daily Elevator Minutes Breakdown")
        ax1.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_idle_steps)))
        ax1.set_title("Minutes Idle")
        ax2.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_active_steps)))
        ax2.set_title("Minutes Active")
        ax3.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_stopped_steps)))
        ax3.set_title("Minutes Stopped")

        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Average Daily Person Minutes Breakdown')
        ax1.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_person_traveling_steps)))
        ax1.set_title("Minutes Traveling")
        ax2.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_person_waiting_steps)))
        ax2.set_title("Minutes Waiting")

        plt.show()
        """
        plt.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_idle_steps)))
        plt.title("Average Daily Elevator Minutes Idle")
        plt.show()

        plt.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_active_steps)))
        plt.title("Average Daily Elevator Minutes Active")
        plt.show()

        plt.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_elevator_stopped_steps)))
        plt.title("Average Daily Elevator Minutes Stopped")
        plt.show()

        plt.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_person_traveling_steps)))
        plt.title("Average Daily Person Minutes Traveling")
        plt.show()

        plt.plot(constants.days_of_week_abbreviations, list(map(self.steps_to_minutes, self.daily_avg_person_waiting_steps)))
        plt.title("Average Daily Person Minutes Waiting")
        plt.show()
        """
    
    """
    Graphs all daily hourly averages.
    """
    def graph_hourly_minute_averages(self):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle("Average Hourly Elevator Minutes Breakdown")
        ax1.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_idle_steps)))
        ax1.set_title("Minutes Idle")
        ax2.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_active_steps)))
        ax2.set_title("Minutes Active")
        ax3.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_stopped_steps)))
        ax3.set_title("Minutes Stopped")

        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Average Hourly Person Minutes Breakdown')
        ax1.plot(list(map(self.steps_to_minutes, self.hourly_avg_person_traveling_steps)))
        ax1.set_title("Minutes Traveling")
        ax2.plot(list(map(self.steps_to_minutes, self.hourly_avg_person_waiting_steps)))
        ax2.set_title("Minutes Waiting")

        plt.show()

        """
        plt.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_idle_steps)))
        plt.title("Average Hourly Elevator Minutes Idle")
        plt.show()

        plt.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_active_steps)))
        plt.title("Average Hourly Elevator Minutes Active")
        plt.show()

        plt.plot(list(map(self.steps_to_minutes, self.hourly_avg_elevator_stopped_steps)))
        plt.title("Average Hourly Elevator Minutes Stopped")
        plt.show()

        plt.plot(list(map(self.steps_to_minutes, self.hourly_avg_person_traveling_steps)))
        plt.title("Average Hourly Person Minutes Traveling")
        plt.show()

        plt.plot(list(map(self.steps_to_minutes, self.hourly_avg_person_waiting_steps)))
        plt.title("Average Hourly Person Minutes Waiting")
        plt.show()
        """