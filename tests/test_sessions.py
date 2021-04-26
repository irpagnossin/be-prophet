import unittest
from datetime import datetime
from extract_features import meeting_sessions

class TestSessions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSessions, self).__init__(*args, **kwargs)
        self.sessions = meeting_sessions('tests/data/zoom_log_sample.csv')

    def test_distinguish_students(self):
        self.assertListEqual(
            list(self.sessions.keys()), 
            ['fulano', 'sicrano', 'beltrano@dominio.com']
        )

    def test_student_sessions_are_sorted(self):
        fulano_sessions = self.sessions['fulano']
        self.assertTrue(fulano_sessions[0][0] < fulano_sessions[1][0])
    
    def test_multiple_sessions(self):
        expected_sessions = [
            (datetime(2021, 4, 25, 18, 50), datetime(2021, 4, 25, 19, 30), 40),
            (datetime(2021, 4, 25, 19, 32), datetime(2021, 4, 25, 19, 35), 3),
            (datetime(2021, 4, 25, 19, 45), datetime(2021, 4, 25, 21, 30), 105)
        ]

        for i, session in enumerate(self.sessions['fulano']):
            self.assertTupleEqual(session, expected_sessions[i])

    def test_it_gives_priority_to_email_over_name(self):
        with self.assertRaises(KeyError):
            self.sessions['beltrano']
        
        self.assertListEqual(
            self.sessions['beltrano@dominio.com'],
            [(datetime(2021, 4, 25, 19, 10), datetime(2021, 4, 25, 21, 30), 140)]
        )
        