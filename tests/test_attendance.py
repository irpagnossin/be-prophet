import unittest
from datetime import datetime
from extract_features import attendance

class TestAttendance(unittest.TestCase):
    def test_student_was_not_present(self):
        student_sessions = []
        self.assertEqual(attendance(student_sessions, 100), 0)
    
    def test_one_session(self):
        student_sessions = [(None, None, 30)]
        self.assertEqual(attendance(student_sessions, 100), 0.3)
    
    def test_many_sessions(self):
        student_sessions = [(None, None, 30), (None, None, 40)]
        self.assertEqual(attendance(student_sessions, 100), 0.7)
    
    def test_lower_limit(self):
        student_sessions = [(None, None, -30), (None, None, 10)]
        self.assertEqual(attendance(student_sessions, 100), 0)

    def test_upper_limit(self):
        student_sessions = [(None, None, 30), (None, None, 40), (None, None, 31)]
        self.assertEqual(attendance(student_sessions, 100), 1)
