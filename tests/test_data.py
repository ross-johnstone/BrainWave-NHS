import unittest
import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
from data import open_project
import datetime
import numpy as np


class Test_Data(unittest.TestCase):

    def setUp(self):
        data, timestamps, annotations = open_project("./data/recording2/pat2/")
        self.data = data
        self.timestamps = timestamps
        self.annotations = annotations

    def test_get_initial_timestamp(self):
        initial_time = self.timestamps[0]
        self.assertEqual(isinstance(initial_time, datetime.datetime), True, "Should be a timestamp")
        self.assertEqual(str(initial_time), "2008-04-02 16:24:49", "Should be: 2008-04-02 16:24:49")

    def test_timestamps_correctness(self):
        for i in range(1, len(self.timestamps)):
            previous_timestamp = self.timestamps[i - 1]
            current_timestamp = self.timestamps[i]
            self.assertEqual(isinstance(current_timestamp, datetime.datetime), True, "Should be a timestamp")
            self.assertEqual(current_timestamp - datetime.timedelta(microseconds=1000 * 20), previous_timestamp,
                             "Should be the same")

    def test_read_wav(self):
        self.assertEqual(issubclass(np.dtype('int32').type, np.integer), True, "Should be an array of integers")


if __name__ == '__main__':
    unittest.main()
