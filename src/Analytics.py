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

    def steps_to_seconds(self, steps):
        return steps * constants.seconds_per_step

    def steps_to_minutes(self, steps):
        return (steps * constants.seconds_per_step) / 60


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


    def evaluate_simulation(self, building, day, step):
        if self.cur_day != day:
            self.cur_day = day
            self.compute_daily_step_averages(building)

        if (step + 1) % 1029 == 0:
            self.compute_hourly_step_averages(building)
        return

    def graph_daily_step_averages(self):
        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], self.daily_avg_elevator_idle_steps)
        plt.title("Average Daily Elevator Steps Idle")
        plt.show()

        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], self.daily_avg_elevator_active_steps)
        plt.title("Average Daily Elevator Steps Active")
        plt.show()

        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], self.daily_avg_elevator_stopped_steps)
        plt.title("Average Daily Elevator Steps Stopped")
        plt.show()

        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], self.daily_avg_person_traveling_steps)
        plt.title("Average Daily Person Steps Traveling")
        plt.show()

        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], self.daily_avg_person_waiting_steps)
        plt.title("Average Daily Person Steps Waiting")
        plt.show()
    
    def graph_hourly_step_averages(self):
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
        plt.show()

    def graph_daily_minute_averages(self):
        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], list(map(self.steps_to_minutes, self.daily_avg_elevator_idle_steps)))
        plt.title("Average Daily Elevator Minutes Idle")
        plt.show()

        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], list(map(self.steps_to_minutes, self.daily_avg_elevator_active_steps)))
        plt.title("Average Daily Elevator Minutes Active")
        plt.show()

        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], list(map(self.steps_to_minutes, self.daily_avg_elevator_stopped_steps)))
        plt.title("Average Daily Elevator Minutes Stopped")
        plt.show()

        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], list(map(self.steps_to_minutes, self.daily_avg_person_traveling_steps)))
        plt.title("Average Daily Person Minutes Traveling")
        plt.show()

        plt.plot(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], list(map(self.steps_to_minutes, self.daily_avg_person_waiting_steps)))
        plt.title("Average Daily Person Minutes Waiting")
        plt.show()
    
    def graph_hourly_minute_averages(self):
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