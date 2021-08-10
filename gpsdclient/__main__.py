import argparse

from . import GPSDClient


def run(args):
    client = GPSDClient()
    for x in client.dict_stream():
        print(x)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-H", "--host", default="127.0.0.1", help="The host running gpsd")
parser.add_argument("-P", "--port", default="2947", help="GPSD port")
parser.add_argument("-J", "--json", action="store_true", help="Output as JSON strings")
parser.add_argument(
    "-F",
    "--filter",
    default="TPV",
    help="""
        Only show specific GPS messages.
        Pass a comma separated list to show multiple message types (e.g. --filter="TSV,SAX").
        To show all messages, set --filter="".
    """,
)
args = parser.parse_args()
print(args)
