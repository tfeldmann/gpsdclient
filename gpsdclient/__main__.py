"""
Shows human-readable gps output.
"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from . import GPSDClient


INDENT = "    "
TPV_FIELDS = "mode time lat lon speed track alt".split()


def report_version(data):
    print("Connected to gpsd v%s" % data["release"])


def report_devices(data):
    print("Devices: ")
    for device in data["devices"]:
        print(INDENT + device.get("path", "n/a"))


def report_tpv(data):
    values = [data.get(field, "n/a") for field in TPV_FIELDS]
    print("\t".join(values))


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
                    print("\t".join(TPV_FIELDS))
                    needs_tpv_header = False
                report_tpv(x)


parser = ArgumentParser(
    formatter_class=ArgumentDefaultsHelpFormatter, description=__doc__
)
parser.add_argument("-H", "--host", default="127.0.0.1", help="The host running gpsd")
parser.add_argument("-P", "--port", default="2947", help="GPSD port")
parser.add_argument("-J", "--json", action="store_true", help="Output as JSON strings")
parser.add_argument(
    "-F",
    "--filter",
    default="",
    help="""
        Only show specific GPS messages in --json mode. Pass a comma separated list to
        show multiple message types (e.g. --filter=TPV,SKY,ATT).
    """,
)
args = parser.parse_args()
run(**vars(args))
