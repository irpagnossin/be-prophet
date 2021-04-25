import unittest
from datetime import datetime
from extract_features import early_departure

class TestEarlyDeparture(unittest.TestCase):
    def test_student_left_on_time(self):
        lesson_ends_at = datetime(2021, 4, 24, 21, 15)
        student_left_at = lesson_ends_at
        student_sessions = [(None, student_left_at, None)]
        self.assertEqual(early_departure(student_sessions, lesson_ends_at), 0)
    
    def test_student_left_before_the_end_of_the_class(self):
        lesson_ends_at = datetime(2021, 4, 24, 21, 15)
        student_left_at = datetime(2021, 4, 24, 21, 7, 12)
        student_sessions = [(None, student_left_at, None)]
        self.assertEqual(early_departure(student_sessions, lesson_ends_at), -7.8)

    def test_student_left_after_the_end_of_the_class(self):
        lesson_ends_at = datetime(2021, 4, 24, 21, 15)
        student_left_at = datetime(2021, 4, 24, 21, 18)
        student_sessions = [(None, student_left_at, None)]
        self.assertEqual(early_departure(student_sessions, lesson_ends_at), 3)