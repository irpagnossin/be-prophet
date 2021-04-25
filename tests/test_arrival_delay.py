import unittest
from datetime import datetime
from extract_features import arrival_delay

class TestArrivalDelay(unittest.TestCase):
    def test_student_arrived_on_time(self):
        lesson_starts_at =datetime(2021, 4, 24, 19)
        student_sessions = [(lesson_starts_at, None, None)]
        self.assertEqual(arrival_delay(student_sessions, lesson_starts_at), 0)
    
    def test_student_was_late(self):
        lesson_starts_at =datetime(2021, 4, 24, 19)
        student_arrives_at = datetime(2021, 4, 24, 19, 10, 6)
        student_sessions = [(student_arrives_at, None, None)]
        self.assertEqual(arrival_delay(student_sessions, lesson_starts_at), -10.1)

    def test_student_arrived_early(self):
        lesson_starts_at =datetime(2021, 4, 24, 19)
        student_arrives_at = datetime(2021, 4, 24, 18, 53, 54)
        student_sessions = [(student_arrives_at, None, None)]
        self.assertEqual(arrival_delay(student_sessions, lesson_starts_at), 6.1)