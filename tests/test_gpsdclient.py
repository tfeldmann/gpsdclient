import socket
import threading
import time
from collections import Counter

from gpsdclient import GPSDClient

from .gpsd_fake import GPSD_OUTPUT, VERSION_HEADER, fake_gpsd_server

socket.setdefaulttimeout(10)


def start_fake_server():
    server = threading.Thread(target=fake_gpsd_server)
    server.start()
    time.sleep(1.0)
    while not server.is_alive():
        time.sleep(0.1)


def test_json_stream():
    expected = (VERSION_HEADER.decode("utf-8") + GPSD_OUTPUT).replace("\n\n", "\n")
    start_fake_server()
    client = GPSDClient()
    output = ""
    for row in client.json_stream():
        output += row + "\n"
    assert output == expected


def test_dict_stream():
    start_fake_server()
    client = GPSDClient()
    count = 0
    for row in client.dict_stream():
        if row["class"] == "TPV":
            count += 1
    assert count == 3


def test_dict_filter():
    start_fake_server()
    client = GPSDClient()
    counter = Counter()
    for row in client.dict_stream(filter=["SKY"]):
        counter[row["class"]] += 1
    assert counter["TPV"] == 0
    assert counter["SKY"] == 3

    start_fake_server()
    client = GPSDClient()
    counter = Counter()
    for row in client.dict_stream(filter=["SKY", "TPV"]):
        counter[row["class"]] += 1
    assert counter["TPV"] == 3
    assert counter["SKY"] == 3
