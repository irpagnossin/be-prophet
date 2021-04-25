import unittest
from extract_features import average_session_duration

class TestAverageSessionDuration(unittest.TestCase):
    def test_no_sessions(self):
        sessions = []
        self.assertEqual(average_session_duration(sessions, 999), 0)
    
    def test_one_session(self):
        sessions = [(None, None, 60)]
        self.assertAlmostEqual(average_session_duration(sessions, 100), 0.6)
    
    def test_many_sessions(self):
        sessions = [(None, None, 10), (None, None, 70)]
        self.assertAlmostEqual(average_session_duration(sessions, 100), 0.4)