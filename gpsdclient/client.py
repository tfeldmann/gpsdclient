"""
A simple GPSD client.
"""
import json
import socket
from datetime import datetime

from typing import Iterable, Union, Any


class GPSDClient:
    def __init__(self, host="127.0.0.1", port="2947"):
        self.host = host
        self.port = port
        self.sock = None

    def json_stream(self) -> Iterable[str]:
        self.close()
        self.sock = socket.create_connection(address=(self.host, int(self.port)))
        self.sock.send(b'?WATCH={"enable":true,"json":true}\n')
        expect_version_header = True
        for line in self.sock.makefile("r", encoding="utf-8"):
            json = line.strip()
            if json:
                if expect_version_header and not json.startswith('{"class":"VERSION"'):
                    raise EnvironmentError(
                        "No valid gpsd version header received. Instead received:\n"
                        "%s...\n"
                        "Are you sure you are connecting to gpsd?" % json[:100]
                    )
                expect_version_header = False
                yield json

    def dict_stream(self, convert_datetime: bool = True) -> Iterable[dict]:
        for line in self.json_stream():
            result = json.loads(line)
            if convert_datetime and "time" in result:
                result["time"] = self._convert_datetime(result["time"])
            yield result

    @staticmethod
    def _convert_datetime(x: Any) -> Union[Any, datetime]:
        """converts the input into a `datetime` object if possible."""
        try:
            if isinstance(x, float):
                return datetime.fromtimestamp(x)
            elif isinstance(x, str):
                # time zone information can be omitted because gps always sends UTC.
                return datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            pass
        return x

    def close(self):
        if self.sock:
            self.sock.close()
        self.sock = None

    def __str__(self):
        return "<GPSDClient(host=%s, port=%s)>" % (self.host, self.port)

    def __del__(self):
        self.close()
