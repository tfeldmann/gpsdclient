"""
A simple and lightweight GPSD client.
"""
import json
import re
import socket
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Union

# old versions of gpsd with NTRIP sources emit invalid json which contains trailing
# commas. As the json strings emitted by gpsd are well known to not contain structures
# like `{"foo": ",}"}` it should be safe to remove all commas directly before curly
# braces. (https://github.com/tfeldmann/gpsdclient/issues/1)
REGEX_TRAILING_COMMAS = re.compile(r"\s*,\s*}")

FilterType = Union[str, Iterable[str]]


def parse_datetime(x: Any) -> Union[Any, datetime]:
    """
    tries to convert the input into a `datetime` object if possible.
    """
    try:
        if isinstance(x, float):
            return datetime.utcfromtimestamp(x).replace(tzinfo=timezone.utc)
        elif isinstance(x, str):
            # time zone information can be omitted because gps always sends UTC.
            result = datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")
            result = result.replace(tzinfo=timezone.utc)
            return result
    except ValueError:
        pass
    return x


def create_filter_regex(reports: Union[str, Iterable[str]] = set()) -> str:
    """
    Dynamically assemble a regular expression to match the given report classes.
    This way we don't need to parse the json to filter by report.
    """
    if isinstance(reports, str):
        reports = reports.split(",")
    if reports:
        classes = set(x.strip().upper() for x in reports)
        return r'"class":\s?"(%s)"' % "|".join(classes)
    return r".*"


class GPSDClient:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: Union[str, int] = "2947",
        timeout: Union[float, int, None] = None,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None  # type: Any

    def gpsd_lines(self):
        self.close()
        self.sock = socket.create_connection(
            address=(self.host, int(self.port)),
            timeout=self.timeout,
        )
        self.sock.send(b'?WATCH={"enable":true,"json":true}\n')
        yield from self.sock.makefile("r", encoding="utf-8")

    def json_stream(self, filter: FilterType = set()) -> Iterable[str]:
        filter_regex = re.compile(create_filter_regex(filter))

        expect_version_header = True
        for line in self.gpsd_lines():
            answ = line.strip()
            if answ:
                if expect_version_header and not answ.startswith('{"class":"VERSION"'):
                    raise EnvironmentError(
                        "No valid gpsd version header received. Instead received:\n"
                        "%s...\n"
                        "Are you sure you are connecting to gpsd?" % answ[:100]
                    )
                expect_version_header = False

                if not filter or filter_regex.search(answ):
                    cleaned_json = REGEX_TRAILING_COMMAS.sub("}", answ)
                    yield cleaned_json

    def dict_stream(
        self, *, convert_datetime: bool = True, filter: FilterType = set()
    ) -> Iterable[Dict[str, Any]]:
        for line in self.json_stream(filter=filter):
            result = json.loads(line)
            if convert_datetime and "time" in result:
                result["time"] = parse_datetime(result["time"])
            yield result

    def close(self):
        if self.sock:
            self.sock.close()
        self.sock = None

    def __str__(self):
        return "<GPSDClient(host=%s, port=%s)>" % (self.host, self.port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def __del__(self):
        self.close()
