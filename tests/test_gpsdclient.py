import threading
from collections import Counter
from datetime import UTC, datetime
from typing import Any
from unittest import mock

import pytest
from gpsdclient import GPSDClient
from gpsdclient.client import parse_datetime

from ._fake_server import GPSD_OUTPUT, VERSION_HEADER, fake_server


@pytest.fixture
def mock_client():
    with (
        mock.patch.object(
            GPSDClient,
            "gpsd_lines",
            return_value=(VERSION_HEADER + GPSD_OUTPUT).splitlines(),
        ),
        GPSDClient() as client,
    ):
        yield client


@pytest.fixture
def server_client():
    ready = threading.Event()
    server = threading.Thread(target=fake_server, args=(ready,), daemon=True)
    server.start()

    # wait until the server socket is listening
    assert ready.wait(timeout=5.0), "fake server did not start"

    with GPSDClient(port=20000) as client:
        yield client
    server.join(timeout=5.0)


FILTER_TESTCASES: Any = (
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
        ("2021-08-13T09:12:42.000Z", datetime(2021, 8, 13, 9, 12, 42, 0, UTC)),
        ("2021-08-13T09:12:42Z", datetime(2021, 8, 13, 9, 12, 42, 0, UTC)),
        ("2021-08-13T09:12:42.5Z", datetime(2021, 8, 13, 9, 12, 42, 500000, UTC)),
        (1662215327, datetime(2022, 9, 3, 14, 28, 47, 0, UTC)),
        (True, True),
        (1662215327.967219, datetime(2022, 9, 3, 14, 28, 47, 967219, UTC)),
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


def test_close_releases_socket_and_file(server_client):
    stream = server_client.json_stream()
    next(stream)
    sock, file = server_client.sock, server_client._file
    server_client.close()
    assert server_client.sock is None and server_client._file is None
    assert file.closed
    assert sock.fileno() == -1


def test_cli_time_column_handles_strings():
    from gpsdclient.cli import print_tpv_row

    # must not raise if the time could not be converted to a datetime
    print_tpv_row({"time": "garbage", "mode": 3})


def test_cli_reports_unexpected_errors(capsys):
    from gpsdclient import cli

    with mock.patch.object(cli, "stream_readable", side_effect=ValueError("boom")):
        with mock.patch("sys.argv", ["gpsdclient"]):
            assert cli.main() == 2
    assert "boom" in capsys.readouterr().err
