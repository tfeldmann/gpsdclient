import threading
import time
from collections import Counter
from datetime import datetime, timezone
from typing import Any
from unittest import mock

import pytest
from gpsdclient import GPSDClient
from gpsdclient.client import parse_datetime

from ._fake_server import GPSD_OUTPUT, VERSION_HEADER, fake_server


@pytest.fixture
def mock_client():
    with mock.patch.object(
        GPSDClient,
        "gpsd_lines",
        return_value=(VERSION_HEADER + GPSD_OUTPUT).splitlines(),
    ):
        with GPSDClient() as client:
            yield client


@pytest.fixture
def server_client():
    server = threading.Thread(target=fake_server)
    server.start()

    # wait for server thread coming alive
    time.sleep(1.0)
    while not server.is_alive():
        time.sleep(0.1)

    with GPSDClient(port=20000) as client:
        yield client


FILTER_TESTCASES: Any
FILTER_TESTCASES = (
    ([], 9),
    (["TPV", "SKY"], 6),
    ("TPV,SKY", 6),
    (["TPV"], 3),
    ("TPV", 3),
    (["SKY"], 3),
    ("SKY", 3),
)


@pytest.mark.parametrize("filter,count", FILTER_TESTCASES)
def test_json_stream_filter(mock_client: GPSDClient, filter, count):
    lines = list(mock_client.json_stream(filter=filter))
    assert len(lines) == count


@pytest.mark.parametrize("filter,count", FILTER_TESTCASES)
def test_dict_stream_filter(mock_client: GPSDClient, filter, count):
    lines = list(mock_client.dict_stream(filter=filter))
    assert len(lines) == count


@pytest.mark.parametrize(
    "input,output",
    (
        ("2021-08-13T09:12:42.000Z", datetime(2021, 8, 13, 9, 12, 42, 0, timezone.utc)),
        (1662215327.967219, datetime(2022, 9, 3, 14, 28, 47, 967219, timezone.utc)),
        ("yesterday", "yesterday"),
        (object, object),
    ),
)
def test_parse_datetime(input, output):
    assert output == parse_datetime(input)


@pytest.mark.parametrize(
    "convert,timetype",
    (
        (True, datetime),
        (False, str),
    ),
)
def test_dict_time_conversion(mock_client: GPSDClient, convert, timetype):
    for line in mock_client.dict_stream(filter="TPV", convert_datetime=convert):
        if "time" in line:
            assert isinstance(line["time"], timetype)


def test_json_stream(server_client):
    expected = (VERSION_HEADER + GPSD_OUTPUT).replace("\n\n", "\n")
    output = ""
    for row in server_client.json_stream():
        output += row + "\n"
    assert output == expected


def test_dict_stream(server_client):
    count = 0
    for row in server_client.dict_stream():
        if row["class"] == "TPV":
            count += 1
    assert count == 3


def test_dict_filter(server_client):
    counter = Counter()
    for row in server_client.dict_stream(filter=["SKY"]):
        counter[row["class"]] += 1
    assert counter["TPV"] == 0
    assert counter["SKY"] == 3


def test_dict_filter_multiple(server_client):
    counter = Counter()
    for row in server_client.dict_stream(filter=["SKY", "TPV"]):
        counter[row["class"]] += 1
    assert counter["TPV"] == 3
    assert counter["SKY"] == 3
