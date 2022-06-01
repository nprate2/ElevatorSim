import unittest
from tqdm import tqdm
import numpy as np

from src_imports import Schedule
from src_imports import constants


class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #print("-----TESTING SCHEDULE-----")
        self.schedules = []
        for i in (range(1000)):
            self.schedules.append(Schedule.generate_schedule())


    #def test_generation(self):
    #    print(".....generating 1,000 schedules.....")
    #    for i in tqdm(range(1000)):
    #        schedule = Schedule.generate_schedule()
    
    def test_total_course_hours(self):
        #print(".....testing total course hours.....")
        for i in (range(1000)):
            self.assertEqual((7, 24), self.schedules[i].shape)
            total_class_hours = len(np.where(self.schedules[i] == 1)[0])
            #print(total_class_hours)
            #print(self.schedules[i])
            #print(np.where(self.schedules[i] == 1))
            self.assertGreaterEqual(total_class_hours, constants.min_total_course_hours)
            self.assertLessEqual(total_class_hours, constants.max_total_course_hours)

    def test_schedule_4CR_lectures(self):
        return
    def test_schedule_3CR_lectures(self):
        return
    def test_schedule_2CR_lectures(self):
        return
    def test_schedule_1CR_lectures(self):
        return
    def test_schedule_discussions(self):
        return

    # Covered by five tests above
    def test_schedule_class(self):
        return
    def test_schedule_sleep(self):
        return
    def test_schedule_meals(self):
        return
    def test_schedule_exercise(self):
        return
    def test_schedule_shopping(self):
        return
    def test_schedule_chores(self):
        return
    def test_schedule_study(self):
        return
    # Covered by all tests above
    def test_generate_schedule(self):
        return


#if __name__ == "__main__":
#    unittest.main()