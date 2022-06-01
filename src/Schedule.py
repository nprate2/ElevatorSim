import numpy as np

import constants

state_name_by_id = {
    0: "freetime",
    1: "class",
    2: "sleep",
    3: "meal",
    4: "exercise",
    5: "shop",
    6: "chores",
    7: "study",
}
state_id_by_name = {
    "freetime": 0,
    "class": 1,
    "sleep": 2,
    "meal": 3,
    "exercise": 4,
    "shop": 5,
    "chores": 6,
    "study": 7
}

"""
Sets lecture times in schedule for 4CR classes

Takes:
class_start_times - numpy array of indices of a schedule day that classes can occurr in
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly

Returns:
Number of discussion sections associated with the chosen course format.
This is used to sum discussions and add them to schedule after all courses' lectures (so discussions don't block a needed lecture time)
"""
def schedule_4CR_lectures(class_start_times, schedule):
    np.random.shuffle(class_start_times)
    # Set the MWF lecture time
    for start_time in class_start_times:
        if schedule[1, start_time] == 0 and schedule[3, start_time] == 0 and schedule[5, start_time] == 0:
            schedule[1, start_time] = state_id_by_name["class"]
            schedule[3, start_time] = state_id_by_name["class"]
            schedule[5, start_time] = state_id_by_name["class"]
            #print("4CR scheduled")
            return 1
    print("4CR unavailable")
    return 0

"""
Sets lecture times in schedule for 3CR classes

Takes:
class_start_times - numpy array of indices of a schedule day that classes can occurr in
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly

Returns:
Number of discussion sections associated with the chosen course format.
This is used to sum discussions and add them to schedule after all courses' lectures (so discussions don't block a needed lecture time)
"""
def schedule_3CR_lectures(class_start_times, schedule):
    np.random.shuffle(class_start_times)
    variety = np.random.randint(low=0, high=3, dtype=int)
    if variety == 0:
        # MWF class
        for start_time in class_start_times:
            if schedule[1, start_time] == 0 and schedule[3, start_time] == 0 and schedule[5, start_time] == 0:
                schedule[1, start_time] = state_id_by_name["class"]
                schedule[3, start_time] = state_id_by_name["class"]
                schedule[5, start_time] = state_id_by_name["class"]
                #print("3CR scheduled MWF")
                return 0
    elif variety == 1:
        # MW class with discussion
        for start_time in class_start_times:
            if schedule[1, start_time] == 0 and schedule[3, start_time] == 0:
                schedule[1, start_time] = state_id_by_name["class"]
                schedule[3, start_time] = state_id_by_name["class"]
                #print("3CR scheduled MW")
                return 1
    else:
        # WF class with discussion
        for start_time in class_start_times:
            if schedule[1, start_time] == 0 and schedule[3, start_time] == 0:
                schedule[1, start_time] = state_id_by_name["class"]
                schedule[3, start_time] = state_id_by_name["class"]
                #print("3CR scheduled WF")
                return 1
    print("3CR unavailable")
    return 0

"""
Sets lecture times in schedule for 2CR classes

Takes:
class_start_times - numpy array of indices of a schedule day that classes can occurr in
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly

Returns:
Number of discussion sections associated with the chosen course format.
This is used to sum discussions and add them to schedule after all courses' lectures (so discussions don't block a needed lecture time)
"""
def schedule_2CR_lectures(class_start_times, schedule):
    np.random.shuffle(class_start_times)
    variety = np.random.randint(low=0, high=2, dtype=int)
    if variety == 0:
        # MW class
        for start_time in class_start_times:
            if schedule[1, start_time] == 0 and schedule[3, start_time] == 0:
                schedule[1, start_time] = state_id_by_name["class"]
                schedule[3, start_time] = state_id_by_name["class"]
                #print("2CR scheduled MW")
                return 0
    else:
        # WF class
        for start_time in class_start_times:
            if schedule[3, start_time] == 0 and schedule[5, start_time] == 0:
                schedule[3, start_time] = state_id_by_name["class"]
                schedule[5, start_time] = state_id_by_name["class"]
                #print("2CR scheduled WF")
                return 0
    print("2CR unavailable")
    return 0

"""
Sets lecture times in schedule for 1CR classes

Takes:
class_start_times - numpy array of indices of a schedule day that classes can occurr in
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly

Returns:
Number of discussion sections associated with the chosen course format.
This is used to sum discussions and add them to schedule after all courses' lectures (so discussions don't block a needed lecture time)
"""
def schedule_1CR_lecture(class_start_times, schedule):
    days = np.linspace(start=1, stop=5, num=5, dtype=int)
    np.random.shuffle(class_start_times)
    # Set class
    for start_time in class_start_times:
        np.random.shuffle(days)
        for day in days:
            if schedule[day, start_time] == 0:
                schedule[day, start_time] = state_id_by_name["class"]
                #print("1CR scheduled")
                return 0
    print("1CR unavailable")
    return 0

"""
Sets discussion times in schedule

Takes:
class_start_times - numpy array of indices of a schedule day that classes can occurr in
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly
num_discussions - cumulative sum of all discussions associated with a person's schedule. This is obtained by summing the return values of schedule_XCR_lecture functions.
"""
def schedule_discussions(class_start_times, schedule, num_discussions):
    days = np.linspace(start=1, stop=5, num=5, dtype=int)
    # Set discussions
    for i in range(num_discussions):
        set = False
        np.random.shuffle(class_start_times)
        for start_time in class_start_times:
            np.random.shuffle(days)
            for day in days:
                if schedule[day, start_time] == 0:
                    schedule[day, start_time] = state_id_by_name["class"]
                    #print("Discussion scheduled")
                    set = True
                    break
            if set:
                break
        if not set:
            print("Discussion unavailable")
            
    return

"""
Generates a random class schedule and stores it in schedule.

Takes:
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly
"""
def schedule_class(schedule):
    total_credit_hours = np.random.randint(constants.min_total_course_hours, constants.max_total_course_hours + 1) # Must add one to max since randint is exclusive for upper limit parameter.
    course_hours = [] # List of credit hours of classes
    hours_left = total_credit_hours
    while (hours_left != 0):
        course_hour = np.random.choice([min(hours_left, 3), min(hours_left, 4)]) # randomly pick either a 3 or 4 credit hour class
        course_hours.append(course_hour)
        hours_left -= course_hour 
    #print("Total CR:", total_credit_hours)
    #print("Course CRs:", course_hours)
    # For each course hour, fit it into the schedule

    class_start_times = np.linspace(start=constants.earliest_course_start, stop=constants.latest_course_start, num=constants.latest_course_start-constants.earliest_course_start, dtype=int) # Hours that classes can start on
    num_discussions = 0
    for i in range(len(course_hours)):
        course_hour = course_hours[i]
        if course_hour == 4:
            num_discussions += schedule_4CR_lectures(class_start_times, schedule)

        elif course_hour == 3:
            num_discussions += schedule_3CR_lectures(class_start_times, schedule)

        elif course_hour == 2:
            num_discussions += schedule_2CR_lectures(class_start_times, schedule)

        else:
            num_discussions += schedule_1CR_lecture(class_start_times, schedule)

    schedule_discussions(class_start_times, schedule, num_discussions)

"""
Generates a random sleep schedule and stores it in schedule.

Takes:
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly
"""
def schedule_sleep(schedule):
    variety = np.random.randint(0, 2)
    if variety == 0:
        # Night Owl - Wakes up an hour before first class each day. If no class a given day, wakes up between 10am-2pm. General sleep pattern is irratic. 5-9 hours of sleep each night
        for i in range(schedule.shape[0]):
            if state_id_by_name["class"] in schedule[i]:
                #print("Class")
                # School day (mostly weekdays)
                sleep_amount = np.random.randint(5, 10)
                first_class_time = np.where(schedule[i]==1)[0][0]
                wakeup_time = first_class_time - 1
                last_sleep_hour = wakeup_time - 1

                if sleep_amount > last_sleep_hour:
                    schedule[i][0:wakeup_time] = state_id_by_name["sleep"]
                    remaining = sleep_amount - last_sleep_hour
                    schedule[i-1][24-remaining:,] = state_id_by_name["sleep"]
                else:
                    first_sleep_hour = last_sleep_hour - sleep_amount
                    schedule[i, first_sleep_hour:wakeup_time] = state_id_by_name["sleep"]
                
            else:
                #print("No Class")
                # No school day (mostly weekends)
                sleep_amount = np.random.randint(6, 11) # 6-10 hours of sleep a night
                wakeup_time = np.random.randint(10, 15) # Wakes up between 10am-2pm
                last_sleep_hour = wakeup_time - 1

                if sleep_amount > last_sleep_hour:
                    schedule[i][0:wakeup_time] = state_id_by_name["sleep"]
                    remaining = sleep_amount - last_sleep_hour
                    schedule[i-1][24-remaining:,] = state_id_by_name["sleep"]
                else:
                    first_sleep_hour = last_sleep_hour - sleep_amount
                    schedule[i, first_sleep_hour:wakeup_time] = state_id_by_name["sleep"]

    else:
        # Early bird. Wakes up between 5-9am, but wakes up at same time each day. Sleeps 7-9 hours each night, general sleep pattern is consistent
        # Upper limit restricted by earliest class time (must wake up at least an hour before earliest class of week)
        earliest_class_time = min(np.where(schedule==state_id_by_name["class"])[1])
        wakeup_time = np.random.randint(5, min(10, earliest_class_time))
        for i in range(schedule.shape[0]):
            last_sleep_hour = wakeup_time - 1
            sleep_amount = np.random.randint(7, 10)
            if sleep_amount > last_sleep_hour:
                schedule[i][0:wakeup_time] = state_id_by_name["sleep"]
                remaining = sleep_amount - last_sleep_hour
                schedule[i-1][24-remaining:,] = state_id_by_name["sleep"]
            else:
                first_sleep_hour = last_sleep_hour - sleep_amount
                schedule[i, first_sleep_hour:wakeup_time] = state_id_by_name["sleep"]

"""
Generates a random meal schedule (breakfast, lunch, dinner, late night) and stores it in schedule.

Takes:
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly
"""
def schedule_meals(schedule):
    for i in range(schedule.shape[0]):
        # For each day, try to set breakfast, lunch, and dinner
        wakeup_time = max(np.where(schedule[i, :15]==state_id_by_name["sleep"])[0]) + 1 # schedule is indexed as such because the latest time a person can wake up is 2pm, i.e. 14
        # Breakfast can happen within the first 3 hours of waking up, lunch within the next 5 hours, dinner within the next 6. 
        breakfast_times = np.linspace(start=wakeup_time, stop=wakeup_time+2, num=3, dtype=int)
        np.random.shuffle(breakfast_times)
        lunch_times = np.linspace(wakeup_time+3, wakeup_time+7, 5, dtype=int)
        np.random.shuffle(lunch_times)
        dinner_times = np.linspace(wakeup_time+8, wakeup_time+13, 6, dtype=int)
        np.random.shuffle(dinner_times)
        for breakfast_time in breakfast_times:
            if schedule[i, breakfast_time] == 0:
                schedule[i, breakfast_time] = state_id_by_name["meal"]
                break
        for lunch_time in lunch_times:
            if schedule[i, lunch_time] == 0:
                schedule[i, lunch_time] = state_id_by_name["meal"]
                break
        for dinner_time in dinner_times:
            if dinner_time >= 24:
                # Handles late night dinners that occur in the early AM of the next day
                if schedule[(i+1)%7, dinner_time-24] == 0:
                    schedule[(i+1)%7, dinner_time-24] = state_id_by_name["meal"]
                    break
            else:
                if schedule[i, dinner_time] == 0:
                    schedule[i, dinner_time] = state_id_by_name["meal"]
                    break
    return

"""
Generates a random exercise schedule and stores it in schedule.

Takes:
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly
"""
def schedule_exercise(schedule):
    hours = np.linspace(0, 23, 14, dtype=int)
    for i in range(schedule.shape[0]):
        # Each day there is a 25% chance a person will workout
        variety = np.random.randint(0,4)
        if variety == 0:
            np.random.shuffle(hours)
            for hour in hours:
                if schedule[i, hour] == 0:
                    schedule[i, hour] = state_id_by_name["exercise"]
                    break
    return

"""
Generates a random shopping schedule and stores it in schedule.

Takes:
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly
"""
def schedule_shopping(schedule):
    hours = np.linspace(0, 23, 14, dtype=int)
    for i in range(schedule.shape[0]):
        # Each day there is a 20% chance a person will go shopping
        variety = np.random.randint(0,5)
        if variety == 0:
            np.random.shuffle(hours)
            for hour in hours:
                if schedule[i, hour] == 0:
                    schedule[i, hour] = state_id_by_name["shop"]
                    break
    return


"""
Generates a random chores schedule and stores it in schedule.

Takes:
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly
"""
def schedule_chores(schedule):
    hours = np.linspace(0, 23, 14, dtype=int)
    for i in range(schedule.shape[0]):
        # Each day there is a 50% chance a person will do chores
        variety = np.random.randint(0,2)
        if variety == 0:
            np.random.shuffle(hours)
            for hour in hours:
                if schedule[i, hour] == 0:
                    schedule[i, hour] = state_id_by_name["chores"]
                    break
    return

"""
Generates a random study schedule and stores it in schedule.

Takes:
schedule - 2d numpy array of shape (7, N) where N is the number of time chunks in each of a week's seven days. If N=24, the schedule is hourly
"""
def schedule_study(schedule):
    hours = np.linspace(0, 23, 14, dtype=int)
    for i in range(schedule.shape[0]):
        for j in range(schedule.shape[1]):
            if schedule[i, j] == 0:
                # Each hour of freetime will be used to study 25% of the time
                if np.random.randint(0,4) == 0:
                    schedule[i, j] == state_id_by_name["study"]
    return

"""
Using the "schedule_[activity]" functions above, a randomized student schedule is generated.
"""
def generate_schedule():
    schedule = np.zeros((7, 24), dtype=int) # 24 hours in a day, 7 days a week
    schedule_class(schedule)
    schedule_sleep(schedule)
    schedule_meals(schedule)
    schedule_exercise(schedule)
    schedule_shopping(schedule)
    schedule_chores(schedule)
    schedule_study(schedule)
    #print("schedule", schedule)
    return schedule

    

#schedule = generate_schedule()
#print("shedule", schedule)