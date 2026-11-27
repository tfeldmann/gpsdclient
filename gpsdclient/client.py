"""
A simple and lightweight GPSD client.
"""

import json
import re
import socket
from collections.abc import Iterable, Iterator
from datetime import UTC, datetime
from typing import Any, Union

# old versions of gpsd with NTRIP sources emit invalid json which contains trailing
# commas. As the json strings emitted by gpsd are well known to not contain structures
# like `{"foo": ",}"}` it should be safe to remove all commas directly before curly
# braces. (https://github.com/tfeldmann/gpsdclient/issues/1)
REGEX_TRAILING_COMMAS = re.compile(r"\s*,\s*}")

FilterType = Union[str, Iterable[str]]


def parse_datetime(x: Any) -> Any | datetime:
    """
    tries to convert the input into a `datetime` object if possible.
    """
    try:
        if isinstance(x, (int, float)) and not isinstance(x, bool):
            return datetime.fromtimestamp(x, UTC)
        elif isinstance(x, str):
            # handles both "...:42.000Z" and "...:42Z"
            result = datetime.fromisoformat(x)
            if result.tzinfo is None:
                # gpsd always sends UTC
                result = result.replace(tzinfo=UTC)
            return result
    except (ValueError, OverflowError, OSError):
        pass
    return x


def create_filter_regex(reports: str | Iterable[str] = set()) -> str:
    """
    Dynamically assemble a regular expression to match the given report classes.
    This way we don't need to parse the json to filter by report.
    """
    if isinstance(reports, str):
        reports = reports.split(",")
    if reports:
        classes = {x.strip().upper() for x in reports}
        return r'"class":\s?"({})"'.format("|".join(classes))
    return r".*"


class GPSDClient:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: str | int = "2947",
        timeout: float | None = None,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None  # type: Any
        self._file = None  # type: Any

    def gpsd_lines(self) -> Iterator[str]:
        self.close()
        self.sock = socket.create_connection(
            address=(self.host, int(self.port)),
            timeout=self.timeout,
        )
        self.sock.sendall(b'?WATCH={"enable":true,"json":true}\n')
        self._file = self.sock.makefile("r", encoding="utf-8")
        yield from self._file

    def json_stream(self, filter: FilterType = set()) -> Iterable[str]:
        filter_regex = re.compile(create_filter_regex(filter))

        expect_version_header = True
        for line in self.gpsd_lines():
            answ = line.strip()
            if answ:
                if expect_version_header and not answ.startswith('{"class":"VERSION"'):
                    raise OSError(
                        "No valid gpsd version header received. Instead received:\n"
                        f"{answ[:100]}...\n"
                        "Are you sure you are connecting to gpsd?"
                    )
                expect_version_header = False

                if not filter or filter_regex.search(answ):
                    cleaned_json = REGEX_TRAILING_COMMAS.sub("}", answ)
                    yield cleaned_json

    def dict_stream(
        self, *, convert_datetime: bool = True, filter: FilterType | None = None
    ) -> Iterable[dict[str, Any]]:
        if filter is None:
            filter = set()
        for line in self.json_stream(filter=filter):
            result = json.loads(line)
            if convert_datetime and "time" in result:
                result["time"] = parse_datetime(result["time"])
            yield result

    def close(self):
        if self._file:
            self._file.close()
        self._file = None
        if self.sock:
            self.sock.close()
        self.sock = None

    def __str__(self):
        return f"<GPSDClient(host={self.host}, port={self.port})>"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def __del__(self):
        self.close()
