"""
Shows human-readable gps output.
"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from . import GPSDClient


def run(args):
    client = GPSDClient()
    for x in client.dict_stream():
        print(x)


parser = ArgumentParser(
    formatter_class=ArgumentDefaultsHelpFormatter, description=__doc__
)
parser.add_argument("-H", "--host", default="127.0.0.1", help="The host running gpsd")
parser.add_argument("-P", "--port", default="2947", help="GPSD port")
parser.add_argument("-J", "--json", action="store_true", help="Output as JSON strings")
parser.add_argument(
    "-F",
    "--filter",
    default="TPV",
    help="""
        Only show specific GPS messages in --json mode.
        Pass a comma separated list to show multiple message types (e.g. --filter="TSV,SAX").
        To show all messages, set --filter="".
    """,
)
args = parser.parse_args()
print(args)
