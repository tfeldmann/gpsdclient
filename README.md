# gpsdclient

[![PyPI Version][pypi-image]][pypi-url]
![PyPI - License](https://img.shields.io/pypi/l/gpsdclient)
[![tests](https://github.com/tfeldmann/gpsdclient/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/tfeldmann/gpsdclient/actions/workflows/tests.yml)

> A small and simple [gpsd](https://gpsd.gitlab.io/gpsd) client and library

## Installation

Needs Python 3 (no other dependencies).
If you want to use the library, use pip:

```
pip3 install gpsdclient
```

If you want to use only the standalone gpsd viewer, I recommend to use pipx:

```
pip3 install pipx
pipx install gpsdclient
```

## Usage in your scripts

```python
from gpsdclient import GPSDClient

client = GPSDClient(host="127.0.0.1")

# get your data as json strings:
for result in client.json_stream():
    print(result)

# or as python dicts (optionally convert time information to `datetime.datetime` objects
for result in client.dict_stream(convert_datetime=True):
    print(result)
```

## Command line usage

You can use the `gpsdclient` standalone program or execute the module with
`python3 -m gpsdclient`.

```
$ gpsdclient --host=192.168.177.151
Connected to gpsd v3.17
Devices: /dev/ttyO4

Mode  Time                  Lat           Lon           Speed   Track   Alt
1     n/a                   n/a           n/a           n/a     n/a     n/a
1     n/a                   n/a           n/a           n/a     n/a     n/a
1     n/a                   n/a           n/a           n/a     n/a     n/a
3     n/a                   51.8131231    6.550163817   n/a     n/a     36.025
3     n/a                   51.8131231    6.550163817   n/a     n/a     36.025
3     2021-08-13 10:43:38   51.8131231    6.550163817   3.071   304.15  36.025
3     2021-08-13 10:43:39   51.813239583  6.550226333   2.665   304.03  36.121
3     2021-08-13 10:43:40   51.813245783  6.550247733   2.418   301.46  36.13
3     2021-08-13 10:43:41   51.813258883  6.550261517   2.13    306.71  36.257
3     2021-08-13 10:43:42   51.81326005   6.55025735    2.413   308.88  36.348
3     2021-08-13 10:43:43   51.813263767  6.550261533   2.557   315.39  36.345
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

## Why

I made this because I just needed a simple client library to read the json data gpsd is
sending.
The other python clients have various problems, like 100 % cpu usage, missing python 3
support, license problems or they aren't available on PyPI. I also wanted a simple gpsd
client to check if everything is working.

This client is as simple as possible with one exception: It supports the automatic
conversion of "time" data into `datetime.datetime` objects.

Have fun, hope you like it.

## License

[MIT](https://choosealicense.com/licenses/mit/)

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/gpsdclient
[pypi-url]: https://pypi.org/project/gpsdclient/
