# gpsdclient

> A small and simple gpsd client for python 3.

This package is in active development and not yet published to PyPI.

## Installation

Needs python 3 installed.

If you want to use the library, use pip:

```
pip3 install gpsdclient
```

If you want to use only the standalone gpsd viewer, I recommend to use pipx:

```
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

## Why

I made this because I just needed a simple client library to read the json data gpsd is
sending.
The other python clients have various problems, like 100 % cpu usage, missing python 3
support, license problems or they aren't available on PyPI. I also wanted a simple gpsd
client to check if everything is working.

This client is as simple as possible with one exception: It supports the automatic
conversion of "time" data into `datetime.datetime` objects.

Have fun, hope you like it.
