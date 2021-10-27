from datetime import datetime
from hashlib import sha1
from dataclasses import dataclass, field
from typing import Optional, Union, List


@dataclass
class JsonRpcRequest:
    id: Union[int, str, None]
    method: str
    params: Optional[str]
    jsonrpc: str = "2.0"


@dataclass
class LoggedTest:
    id: str = field(init=False, default="")
    app_server: str
    api_name: str
    method: str
    parameters: str
    ran_at: datetime
    ran_week: str = field(init=False, default="")
    method_exec_time: float
    logfile_id: int

    def __post_init__(self):
        # id
        id_str = str(self.app_server) + str(self.api_name) + str(self.method) + str(self.parameters) + str(self.logfile_id)
        self.id = sha1(id_str.encode()).hexdigest()
        # ran_week
        dt = self.ran_at.isocalendar()
        self.ran_week = f"{dt.year}W{str(dt.week).zfill(2)}"


@dataclass
class Logfile:
    id: int = field(init=False, default=0)
    path: str
    created: datetime
    hostname: str
    parse_time: datetime
    logged_tests: List[LoggedTest] = field(default_factory=list)








