import unittest
import os
import platform
from datetime import datetime
from parsers.log_parser import parse_logfile_path, parse_request_data_string, parse_response_time_string
from models.data_structures import JsonRpcRequest, Logfile


class TestParseLogfileName(unittest.TestCase):

    def setUp(self):
        self.log_file_path_one = "2021-10-10T15-30-00.log"
        self.log_file_path_two = "/var/log/app_name/2021-10-10T15-00-00.log"
        self.invalid_log_file_path = "invalid_name.log"

    def test_parse_valid_path(self):
        result_one = parse_logfile_path(self.log_file_path_one)
        parse_time = result_one.parse_time
        expected_one = Logfile(
            path=os.path.abspath(self.log_file_path_one),
            created=datetime(year=2021, month=10, day=10, hour=15, minute=30, second=0),
            parse_time=parse_time,
            hostname=platform.node()
        )

        result_two = parse_logfile_path(self.log_file_path_two)
        parse_time = result_two.parse_time
        expected_two = Logfile(
            path=self.log_file_path_two,
            created=datetime(year=2021, month=10, day=10, hour=15, minute=0, second=0),
            parse_time=parse_time,
            hostname=platform.node()
        )
        # Assertions
        self.assertEqual(result_one, expected_one, f"\n{result_one}\n{expected_one}\n")
        self.assertEqual(result_two, expected_two)

    def test_parse_path(self):
        with self.assertRaises(ValueError):
            parse_logfile_path(self.invalid_log_file_path)


class TestParseRequestDataString(unittest.TestCase):
    def setUp(self):
        self.request_data_string_one = """Sending {"jsonrpc": "2.0", "id": "1", "method": "API.some_method", \
        "params": {"param1": "x", "param2": "y", "sort": "blog", "limit": "21"}} for reference time measurement
        """
        self.request_data_string_two = """Sending {"jsonrpc": "2.0", "id": "1", "method": "API2.some_method1", \
            "params": {"param1": "z", "param2": "d", "sort": "blog", "limit": "21"}} for reference time measurement"""
        self.invalid_request_data_string = "Sending invalid reques data string"

    def test_parse_valid_request_data_string(self):
        result_one = parse_request_data_string(self.request_data_string_one)
        expected_one = JsonRpcRequest(
            jsonrpc="2.0",
            id="1",
            method="API.some_method",
            params=str({"param1": "x", "param2": "y", "sort": "blog", "limit": "21"})
        )
        result_two = parse_request_data_string(self.request_data_string_two)
        expected_two = JsonRpcRequest(
            jsonrpc="2.0",
            id="1",
            method="API2.some_method1",
            params=str({"param1": "z", "param2": "d", "sort": "blog", "limit": "21"})
        )
        # Assertions
        self.assertEqual(result_one, expected_one)
        self.assertEqual(result_two, expected_two)

    def test_parse_invalid_request_data_string(self):
        with self.assertRaises(ValueError):
            parse_request_data_string(self.invalid_request_data_string)


class TestParseResponseTimeString(unittest.TestCase):
    def setUp(self):
        self.response_time_string_one = "Got response in 0.6832s"
        self.response_time_string_two = "Got response in 1.2145s"
        self.invalid_response_string = "Invalid response string"

    def test_parse_valid_response_time_string(self):
        result_one = parse_response_time_string(self.response_time_string_one)
        expected_one = 0.6832
        result_two = parse_response_time_string(self.response_time_string_two)
        expected_two = 1.2145

        # Assertions
        self.assertEqual(expected_one, result_one)
        self.assertIsInstance(expected_one, float)
        self.assertEqual(expected_two, result_two)
        self.assertIsInstance(expected_two, float)

    def test_parse_invalid_response_time_string(self):
        with self.assertRaises(ValueError):
            parse_response_time_string(self.invalid_response_string)
