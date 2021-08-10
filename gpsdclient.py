"""
A simple GPSD client.
"""
import json
import socket
from datetime import datetime


class GPSDClient:
    def __init__(self, host="127.0.0.1", port="2947"):
        self.host = host
        self.port = port
        self.sock = None

    def stream(self):
        self.close()
        self.sock = socket.create_connection(address=(self.host, self.port))
        self.sock.send(b'?WATCH={"enable":true,"json":true}\n')
        for line in self.sock.makefile("r", encoding="utf-8"):
            yield line.strip()

    def dict_stream(self, convert_datetime=True):
        for line in self.stream():
            result = json.loads(line)
            if convert_datetime and "time" in result:
                result["time"] = self._convert_datetime(result["time"])
            yield result

    @staticmethod
    def _convert_datetime(x):
        try:
            if isinstance(x, float):
                return datetime.fromtimestamp(x)
            elif isinstance(x, str):
                return datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            pass
        return x

    def close(self):
        if self.sock:
            self.sock.close()
        self.sock = None

    def __del__(self):
        self.close()


if __name__ == "__main__":
    client = GPSDClient()
    for x in client.dict_stream():
        print(x)
