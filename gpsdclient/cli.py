"""
Shows human-readable gps output.
"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys
from . import GPSDClient


COLUMN_GAP = "  "
TPV_DISPLAY = {
    "mode": (4, str),
    "time": (20, lambda x: x.isoformat(sep=" ", timespec="seconds")),
    "lat": (12, str),
    "lon": (12, str),
    "speed": (6, str),
    "track": (6, str),
    "alt": (9, str),
}


def report_version(data):
    print("Connected to gpsd v%s" % data["release"])


def report_devices(data):
    output = ", ".join(x.get("path", "n/a") for x in data["devices"])
    print("Devices: %s" % output)


def report_tpv_header():
    print()
    for key, options in TPV_DISPLAY.items():
        width, _ = options
        print(key.title().ljust(width), end=COLUMN_GAP)
    print()


def report_tpv(data):
    for key, options in TPV_DISPLAY.items():
        width, formatter = options
        if key in data:
            value = formatter(data[key])
        else:
            value = "n/a"
        print(value.ljust(width), end=COLUMN_GAP)
    print()


def run(host, port, json, filter):
    filter_topics = set(filter.upper().replace(" ", "").split(","))
    client = GPSDClient(host=host, port=port)

    # JSON (raw) output
    if json:
        for x in client.json_stream():
            # TODO: FILTER
            print(x)

    # human readable output
    else:
        needs_tpv_header = True
        for x in client.dict_stream(convert_datetime=True):
            if x["class"] == "VERSION":
                report_version(x)
                needs_tpv_header = True
            elif x["class"] == "DEVICES":
                report_devices(x)
                needs_tpv_header = True
            elif x["class"] == "TPV":
                if needs_tpv_header:
                    report_tpv_header()
                    needs_tpv_header = False
                report_tpv(x)


def main():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter, description=__doc__
    )
    parser.add_argument(
        "-H", "--host", default="127.0.0.1", help="The host running gpsd"
    )
    parser.add_argument("-P", "--port", default="2947", help="GPSD port")
    parser.add_argument(
        "-J", "--json", action="store_true", help="Output as JSON strings"
    )
    parser.add_argument(
        "-F",
        "--filter",
        default="",
        help="""
            Only show specific GPS messages in --json mode. Pass a comma separated list
            to show multiple message types (e.g. --filter=TPV,SKY,ATT).
        """,
    )
    args = parser.parse_args()
    try:
        run(**vars(args))
    except (ConnectionError, EnvironmentError) as e:
        print(e)
    except KeyboardInterrupt:
        print()
        return 0
