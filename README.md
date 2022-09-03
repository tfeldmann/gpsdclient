# gpsdclient

[![PyPI Version][pypi-version]][pypi-url]
[![PyPI License][pypi-license]][mit-license]
[![tests][test-badge]][test-url]

> A simple and lightweight [gpsd](https://gpsd.gitlab.io/gpsd) client and library

## Installation

Needs Python 3 (no other dependencies).
If you want to use the library, use pip:

```
pip3 install gpsdclient
```

If you want to use only the standalone gpsd viewer, I recommend to use pipx:

```
pipx install gpsdclient
```

## Library usage

```python
from gpsdclient import GPSDClient

# get your data as json strings:
with GPSDClient(host="127.0.0.1") as client:
    for result in client.json_stream():
        print(result)

# or as python dicts (optionally convert time information to `datetime` objects)
with GPSDClient() as client:
    for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
        print("Latitude: %s" % result.get("lat", "n/a"))
        print("Longitude: %s" % result.get("lon", "n/a"))

# you can optionally filter by report class
with GPSDClient() as client:
    for result in client.dict_stream(filter=["TPV", "SKY"]):
        print(result)
```

You can find the documentation for the available data and JSON fields in the
[gpsd_json(5) manpage](https://www.mankier.com/5/gpsd_json).

## Command line usage

You can use the `gpsdclient` standalone program or execute the module with
`python3 -m gpsdclient`.

```
$ gpsdclient
Connected to gpsd v3.17
Devices: /dev/ttyO4

Mode | Time                 | Lat          | Lon          | Speed  | Track  | Alt       | Climb
-----+----------------------+--------------+--------------+--------+--------+-----------+-----------
1    | n/a                  | n/a          | n/a          | n/a    | n/a    | n/a       | n/a
1    | n/a                  | n/a          | n/a          | n/a    | n/a    | n/a       | n/a
1    | n/a                  | n/a          | n/a          | n/a    | n/a    | n/a       | n/a
3    | n/a                  | 51.813360383 | 6.550329033  | n/a    | n/a    | 46.518    | 0.0
3    | n/a                  | 51.813360383 | 6.550329033  | n/a    | n/a    | 46.518    | 0.0
3    | 2021-08-13 14:06:25  | 51.813360383 | 6.550329033  | 0.674  | 260.53 | 46.518    | 0.0
3    | 2021-08-13 14:06:27  | 51.81335905  | 6.550316283  | 0.54   | 245.71 | 46.002    | 0.0
3    | 2021-08-13 14:06:28  | 51.8133673   | 6.55033345   | 0.422  | 241.88 | 46.476    | 0.0
3    | 2021-08-13 14:06:29  | 51.813365833 | 6.5503352    | 0.34   | 246.35 | 46.868    | 0.0
3    | 2021-08-13 14:06:30  | 51.81336285  | 6.550339117  | 0.242  | 246.35 | 47.22     | 0.0
3    | 2021-08-13 14:06:31  | 51.8133614   | 6.550350367  | 0.273  | 246.35 | 46.846    | 0.0
3    | 2021-08-13 14:06:32  | 51.813359233 | 6.550353767  | 0.226  | 246.35 | 46.635    | 0.0
3    | 2021-08-13 14:06:33  | 51.8133574   | 6.550349817  | 0.221  | 246.35 | 46.52     | 0.0
3    | 2021-08-13 14:06:34  | 51.813356733 | 6.550345917  | 0.319  | 274.21 | 46.453    | 0.0
3    | 2021-08-13 14:06:35  | 51.813357917 | 6.5503521    | 0.149  | 274.21 | 46.529    | 0.0
^C
```

Or use the raw json mode:

```json
$ gpsdclient --json
{"class":"VERSION","release":"3.17","rev":"3.17","proto_major":3,"proto_minor":12}
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/ttyO4","driver":"NMEA0183","activated":"2021-08-13T12:25:00.896Z","flags":1,"native":0,"bps":9600,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}
{"class":"SKY","device":"/dev/ttyO4","xdop":0.87,"ydop":1.86,"vdop":0.93,"tdop":2.26,"hdop":1.36,"gdop":3.96,"pdop":1.65,"satellites":[{"PRN":1,"el":84,"az":318,"ss":22,"used":true},{"PRN":22,"el":78,"az":234,"ss":16,"used":true},{"PRN":21,"el":72,"az":115,"ss":0,"used":false},{"PRN":3,"el":55,"az":239,"ss":19,"used":true},{"PRN":17,"el":34,"az":309,"ss":20,"used":true},{"PRN":32,"el":32,"az":53,"ss":32,"used":true},{"PRN":8,"el":21,"az":172,"ss":13,"used":false},{"PRN":14,"el":18,"az":274,"ss":13,"used":false},{"PRN":131,"el":10,"az":115,"ss":0,"used":false},{"PRN":19,"el":9,"az":321,"ss":33,"used":true},{"PRN":4,"el":4,"az":187,"ss":0,"used":false},{"PRN":31,"el":1,"az":106,"ss":0,"used":false},{"PRN":69,"el":80,"az":115,"ss":17,"used":true},{"PRN":84,"el":73,"az":123,"ss":0,"used":false},{"PRN":85,"el":42,"az":318,"ss":26,"used":true},{"PRN":68,"el":33,"az":39,"ss":0,"used":false},{"PRN":70,"el":27,"az":208,"ss":0,"used":false},{"PRN":76,"el":12,"az":330,"ss":19,"used":true},{"PRN":83,"el":12,"az":133,"ss":16,"used":false},{"PRN":77,"el":9,"az":18,"ss":0,"used":false}]}
{"class":"TPV","device":"/dev/ttyO4","mode":3,"time":"2021-08-13T12:25:01.000Z","ept":0.005,"lat":51.813525983,"lon":6.550081367,"alt":63.037,"epx":13.150,"epy":27.967,"epv":21.390,"track":211.3400,"speed":0.000,"climb":0.000,"eps":62.58,"epc":42.78}
^C
```

All command line options:

```
$ gpsdclient -h
usage: gpsdclient [-h] [--host HOST] [--port PORT] [--json]

Connect to a running gpsd instance and show human readable output.

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  The host running GPSD (default: 127.0.0.1)
  --port PORT  GPSD port (default: 2947)
  --json       Output as JSON strings (default: False)
```

## Why

I made this because I just needed a simple client library to read the json data gpsd is
sending.
The other python libraries have various problems, like 100 % cpu usage, missing python 3
support, license problems, lots of dependencies or they aren't available on PyPI.
I also wanted a simple gpsd client to check if everything is working.

This client is as simple as possible with one exception: It supports the automatic
conversion of "time" data into `datetime.datetime` objects.

Have fun, hope you like it.

## License

[MIT][mit-license]

<!-- Badges -->

[pypi-version]: https://img.shields.io/pypi/v/gpsdclient
[pypi-license]: https://img.shields.io/pypi/l/gpsdclient
[pypi-url]: https://pypi.org/project/gpsdclient/
[mit-license]: https://choosealicense.com/licenses/mit/
[test-badge]: https://github.com/tfeldmann/gpsdclient/actions/workflows/tests.yml/badge.svg?branch=main
[test-url]: https://github.com/tfeldmann/gpsdclient/actions/workflows/tests.yml
