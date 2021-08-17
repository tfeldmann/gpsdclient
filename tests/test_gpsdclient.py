import socket
import threading
import time

from gpsdclient import GPSDClient

from .gpsd_fake import fake_gpsd_server, VERSION_HEADER, GPSD_OUTPUT

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
