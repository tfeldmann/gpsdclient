# gpsdclient

A small and simple gpsd client for python 3.

This package is in active development and not yet published to PyPI.

## Usage

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

## Why

I made this because I just needed a simple client to read the json data gpsd is sending.
The other python clients have various problems, like 100 % cpu usage, missing python 3
support, license problems or aren't available on PyPI.

This client is as simple as possible with one exception: It supports the automatic
conversion of "time" data into `datetime.datetime` objects.

Have fun, hope you like it.
