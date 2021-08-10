# gpsdclient

A small and simple gpsd client for python 3.

```python
from gpsdclient import GPSDClient

client = GPSDClient(host="127.0.0.1")
for result in client.dict_stream(convert_datetime=True):
    print(result)
```
