import sys
import os
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
sys.path.append(os.path.join(dirname(dirname(__file__)), 'res/'))
import numpy as np
import datetime
from data import check_valid_path
from data import open_project
import unittest



class Test_Data(unittest.TestCase):

    def setUp(self):
        self.path = "./data/recording2/pat2/"
        data, timestamps, annotations = open_project(self.path)
        self.data = data
        self.timestamps = timestamps
        self.annotations = annotations

    def test_check_valid_path(self):
        self.assertTrue(
            check_valid_path(
                self.path),
            "Should return true the path is valid")
        self.assertFalse(check_valid_path("/"),
                         "Should return false as no path is given")

    def test_check_valid_path_exceptions(self):
        with self.assertRaises(Exception):
            check_valid_path("./data/invalid_paths/empty")
        with self.assertRaises(Exception):
            check_valid_path("./data/invalid_paths/no_cal_file")
        with self.assertRaises(Exception):
            check_valid_path("./data/invalid_paths/no_wav_file")

    def test_get_initial_timestamp(self):
        initial_time = self.timestamps[0]
        self.assertTrue(
            isinstance(
                initial_time,
                datetime.datetime),
            "Should be a timestamp")
        self.assertEqual(
            str(initial_time),
            "2008-04-02 16:24:49",
            "Should be: 2008-04-02 16:24:49")

    def test_timestamps_correctness(self):
        for i in range(1, len(self.timestamps)):
            previous_timestamp = self.timestamps[i - 1]
            current_timestamp = self.timestamps[i]
            self.assertTrue(
                isinstance(
                    current_timestamp,
                    datetime.datetime),
                "Should be a timestamp")
            self.assertEqual(current_timestamp - datetime.timedelta(microseconds=1000 * 20), previous_timestamp,
                             "Should be the same")

    def test_read_wav(self):
        self.assertTrue(
            issubclass(
                np.dtype('int32').type,
                np.integer),
            "Should be an array of integers")


if __name__ == '__main__':
    unittest.main()
