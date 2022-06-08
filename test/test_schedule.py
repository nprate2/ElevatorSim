import unittest
from tqdm import tqdm
import numpy as np

from src_imports import Schedule
from src_imports import constants


class TestSchedule(unittest.TestCase):
    """
    Before each test, generate 1000 schedules
    """
    @classmethod
    def setUpClass(self):
        self.schedules = []
        for i in (range(1000)):
            self.schedules.append(Schedule.generate_schedule())
    
    """
    Asserts that each Schedule has a total number of class hours that falls between min_total_course_hours and max_total_course_hours
    """
    def test_total_course_hours(self):
        for i in range(len(self.schedules)):
            self.assertEqual((7, 24), self.schedules[i].shape)
            total_class_hours = len(np.where(self.schedules[i] == 1)[0])
            self.assertGreaterEqual(total_class_hours, constants.min_total_course_hours)
            self.assertLessEqual(total_class_hours, constants.max_total_course_hours)

    # Covered by test_total_course_hours
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