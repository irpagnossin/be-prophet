import unittest
from datetime import datetime
from extract_features import time_delta

class TestTimeDelta(unittest.TestCase):
    def test_small_positive_difference(self):
        datetime_1 = datetime(2021, 4, 24, 18, 45)
        datetime_2 = datetime(2021, 4, 24, 19)
        self.assertEqual(time_delta(datetime_1, datetime_2), 15)

    def test_small_negative_difference(self):
        datetime_1 = datetime(2021, 4, 24, 19, 37)
        datetime_2 = datetime(2021, 4, 24, 19)
        self.assertEqual(time_delta(datetime_1, datetime_2), -37)
    
    def test_large_positive_difference(self):
        datetime_1 = datetime(2021, 4, 24, 19)
        datetime_2 = datetime(2021, 4, 25, 19, 0, 1)
        
        expected_delta = (24 * 3600 + 1) / 60
        self.assertAlmostEqual(time_delta(datetime_1, datetime_2), expected_delta)
    
    def test_large_negative_difference(self):
        datetime_1 = datetime(2021, 4, 24, 19)
        datetime_2 = datetime(2021, 4, 23, 19, 0, 1)
        
        expected_delta = -(24 * 3600 - 1) / 60
        self.assertAlmostEqual(time_delta(datetime_1, datetime_2), expected_delta)