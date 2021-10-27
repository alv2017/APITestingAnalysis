import re
import os
import json
import platform
from datetime import datetime
from models.data_structures import JsonRpcRequest, Logfile


def get_api_server_name(log_file: str) -> str:
    pattern = r"https?://\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"
    server_found = None
    line_no = 1
    line_max = 10
    with open(log_file, "r") as lf:
        line = lf.readline()
        while server_found is None and line_no < line_max:
            server_found = re.search(pattern, line)
            line = lf.readline()
            line_no += 1
    if server_found:
        return server_found.group()
    else:
        return 'UNKNOWN'


def parse_logfile_path(log_file: str) -> Logfile:
    """
    The function parses log file path and returns Logfile object
    :param log_file: str: path to log file
    :return: datetime: logging date-time
    """
    pattern = r"(\d{4})-(\d{2})-(\d{2})T(\d{2})-(\d{2})-(\d{2}).log"
    result = re.search(pattern, log_file)
    if result:
        created = datetime(year=int(result.group(1)),
                           month=int(result.group(2)),
                           day=int(result.group(3)),
                           hour=int(result.group(4)),
                           minute=int(result.group(5)),
                           second=int(result.group(6))
                           )
        return Logfile(
            path=os.path.abspath(log_file),
            created=created,
            parse_time=datetime.now(),
            hostname=platform.node(),
        )
    else:
        raise ValueError("Log file name didn't match the pattern")


def parse_request_data_string(request_data: str) -> JsonRpcRequest:
    """
    The function takes request data string as an input and returns JsonRpcRequest object
    :param request_data: str
    :return: JsonRpcRequest object
    """
    pattern = r"Sending (\{\"jsonrpc\":.+\})"
    result = re.match(pattern, request_data)
    if result:
        request_content = result.group(1)
        request_dict = json.loads(request_content)
        return JsonRpcRequest(
            jsonrpc=request_dict["jsonrpc"],
            id=request_dict["id"],
            method=request_dict["method"],
            params=str(request_dict["params"])
        )
    else:
        raise ValueError("String doesn't match the required request data pattern.")


def parse_response_time_string(response_string: str) -> float:
    """
    The function takes the response timing string as an input and returns the response execution time
    :param response_string: str
    :return: float: response execution time
    """
    pattern = r"Got response in (\d\.\d+)"
    result = re.match(pattern, response_string)
    if result:
        return float(result.group(1))
    else:
        raise ValueError("String doesn't match the required response time string pattern.")