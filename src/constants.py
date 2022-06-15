days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
days_of_week_abbreviations = ["Su", "M", "T", "W", "Tr", "F", "Sa"]
seconds_per_step = 3.5 # For the sake of simulation and analytics, number of seconds each simulation step represents

hours_per_day = 24
minutes_per_day = 60 * hours_per_day
seconds_per_day = 60 * minutes_per_day # Number of seconds in a day

minutes_per_hour = minutes_per_day / hours_per_day
seconds_per_hour = 60 * minutes_per_hour

steps_per_day = seconds_per_day / seconds_per_step # Number of simulation steps to represent a 24 hour day
steps_per_hour = steps_per_day / 24

# Determines the range of total number of credit hours a schedule can have
min_total_course_hours = 12
max_total_course_hours = 18 # Schedules may not be generated properly if max exceeds 32

# Determines the range of times that courses can occur within (24 hour schedule)
earliest_course_start = 8 # 8am
latest_course_start = 18 # 6pm