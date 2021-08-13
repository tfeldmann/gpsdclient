import time
import socket
import threading
from gpsdclient import GPSDClient

socket.setdefaulttimeout(10)


VERSION_HEADER = b'{"class":"VERSION","release":"3.17","rev":"3.17","proto_major":3,"proto_minor":12}\n'
WATCH_COMMAND = b'?WATCH={"enable":true,"json":true}\n'
GPSD_OUTPUT = """
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/ttyO4","driver":"NMEA0183","activated":"2021-08-13T09:12:40.028Z","flags":1,"native":0,"bps":9600,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}
{"class":"SKY","device":"/dev/ttyO4","xdop":0.54,"ydop":0.77,"vdop":0.85,"tdop":1.00,"hdop":0.89,"gdop":2.12,"pdop":1.23,"satellites":[{"PRN":27,"el":84,"az":141,"ss":0,"used":false},{"PRN":8,"el":60,"az":294,"ss":16,"used":true},{"PRN":10,"el":60,"az":109,"ss":16,"used":true},{"PRN":23,"el":40,"az":59,"ss":17,"used":false},{"PRN":16,"el":33,"az":188,"ss":26,"used":true},{"PRN":21,"el":28,"az":256,"ss":16,"used":false},{"PRN":18,"el":12,"az":69,"ss":26,"used":true},{"PRN":7,"el":9,"az":288,"ss":0,"used":false},{"PRN":30,"el":9,"az":321,"ss":32,"used":true},{"PRN":15,"el":8,"az":28,"ss":0,"used":false},{"PRN":26,"el":6,"az":175,"ss":0,"used":false},{"PRN":1,"el":3,"az":251,"ss":0,"used":false},{"PRN":32,"el":2,"az":133,"ss":0,"used":false},{"PRN":13,"el":1,"az":2,"ss":0,"used":false},{"PRN":138,"el":0,"az":0,"ss":0,"used":false},{"PRN":83,"el":66,"az":321,"ss":0,"used":false},{"PRN":82,"el":50,"az":68,"ss":0,"used":false},{"PRN":67,"el":43,"az":98,"ss":19,"used":true},{"PRN":73,"el":35,"az":261,"ss":17,"used":true},{"PRN":74,"el":29,"az":320,"ss":21,"used":true},{"PRN":66,"el":27,"az":33,"ss":30,"used":true},{"PRN":68,"el":17,"az":150,"ss":0,"used":false},{"PRN":84,"el":12,"az":279,"ss":0,"used":false},{"PRN":80,"el":11,"az":215,"ss":0,"used":false},{"PRN":81,"el":5,"az":88,"ss":0,"used":false}]}
{"class":"TPV","device":"/dev/ttyO4","mode":3,"time":"2021-08-13T09:12:40.000Z","ept":0.005,"lat":51.813280233,"lon":6.550214200,"alt":30.393,"epx":8.171,"epy":11.499,"epv":19.550,"track":12.4500,"speed":0.000,"climb":0.000,"eps":23.00,"epc":39.10}
{"class":"SKY","device":"/dev/ttyO4","xdop":0.54,"ydop":0.77,"vdop":0.85,"tdop":1.00,"hdop":0.89,"gdop":2.12,"pdop":1.23,"satellites":[{"PRN":27,"el":84,"az":141,"ss":0,"used":false},{"PRN":8,"el":60,"az":294,"ss":16,"used":true},{"PRN":10,"el":60,"az":109,"ss":16,"used":true},{"PRN":23,"el":40,"az":59,"ss":17,"used":false},{"PRN":16,"el":33,"az":188,"ss":26,"used":true},{"PRN":21,"el":28,"az":256,"ss":16,"used":false},{"PRN":18,"el":12,"az":69,"ss":26,"used":true},{"PRN":7,"el":9,"az":288,"ss":0,"used":false},{"PRN":30,"el":9,"az":321,"ss":33,"used":true},{"PRN":15,"el":8,"az":28,"ss":0,"used":false},{"PRN":26,"el":6,"az":175,"ss":0,"used":false},{"PRN":1,"el":3,"az":251,"ss":0,"used":false},{"PRN":32,"el":2,"az":133,"ss":0,"used":false},{"PRN":13,"el":1,"az":2,"ss":0,"used":false},{"PRN":138,"el":0,"az":0,"ss":0,"used":false},{"PRN":83,"el":66,"az":321,"ss":0,"used":false},{"PRN":82,"el":50,"az":68,"ss":0,"used":false},{"PRN":67,"el":43,"az":98,"ss":19,"used":true},{"PRN":73,"el":35,"az":261,"ss":16,"used":true},{"PRN":74,"el":29,"az":320,"ss":21,"used":true},{"PRN":66,"el":27,"az":33,"ss":30,"used":true},{"PRN":68,"el":17,"az":150,"ss":0,"used":false},{"PRN":84,"el":12,"az":279,"ss":0,"used":false},{"PRN":80,"el":11,"az":215,"ss":0,"used":false},{"PRN":81,"el":5,"az":88,"ss":0,"used":false}]}
{"class":"TPV","device":"/dev/ttyO4","mode":3,"time":"2021-08-13T09:12:41.000Z","ept":0.005,"lat":51.813280233,"lon":6.550214200,"alt":30.393,"epx":8.171,"epy":11.499,"epv":19.550,"track":12.4500,"speed":0.000,"climb":0.000,"eps":23.00,"epc":39.10}
{"class":"SKY","device":"/dev/ttyO4","xdop":0.54,"ydop":0.77,"vdop":0.85,"tdop":1.00,"hdop":0.89,"gdop":2.12,"pdop":1.22,"satellites":[{"PRN":27,"el":84,"az":141,"ss":0,"used":false},{"PRN":8,"el":60,"az":294,"ss":16,"used":true},{"PRN":10,"el":60,"az":109,"ss":17,"used":true},{"PRN":23,"el":40,"az":59,"ss":17,"used":false},{"PRN":16,"el":33,"az":188,"ss":26,"used":true},{"PRN":21,"el":28,"az":256,"ss":16,"used":false},{"PRN":18,"el":12,"az":69,"ss":26,"used":true},{"PRN":7,"el":9,"az":288,"ss":0,"used":false},{"PRN":30,"el":9,"az":321,"ss":33,"used":true},{"PRN":15,"el":8,"az":28,"ss":0,"used":false},{"PRN":26,"el":6,"az":175,"ss":0,"used":false},{"PRN":1,"el":3,"az":251,"ss":0,"used":false},{"PRN":32,"el":2,"az":133,"ss":0,"used":false},{"PRN":13,"el":1,"az":2,"ss":0,"used":false},{"PRN":138,"el":0,"az":0,"ss":0,"used":false},{"PRN":83,"el":66,"az":321,"ss":0,"used":false},{"PRN":82,"el":50,"az":68,"ss":0,"used":false},{"PRN":67,"el":43,"az":98,"ss":19,"used":true},{"PRN":73,"el":35,"az":261,"ss":15,"used":true},{"PRN":74,"el":29,"az":320,"ss":21,"used":true},{"PRN":66,"el":27,"az":33,"ss":30,"used":true},{"PRN":68,"el":17,"az":150,"ss":0,"used":false},{"PRN":84,"el":12,"az":279,"ss":0,"used":false},{"PRN":80,"el":11,"az":215,"ss":0,"used":false},{"PRN":81,"el":5,"az":88,"ss":0,"used":false}]}
{"class":"TPV","device":"/dev/ttyO4","mode":3,"time":"2021-08-13T09:12:42.000Z","ept":0.005,"lat":51.813280233,"lon":6.550214200,"alt":30.393,"epx":8.171,"epy":11.499,"epv":19.550,"track":12.4500,"speed":0.000,"climb":0.000,"eps":23.00,"epc":39.10}
"""


def fake_gpsd_server():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(("127.0.0.1", 2947))
    sock.listen(10)
    client, _ = sock.accept()
    client.send(VERSION_HEADER)
    if client.recv(100) == WATCH_COMMAND:
        n = 120
        chunks = [GPSD_OUTPUT[i : i + n] for i in range(0, len(GPSD_OUTPUT), n)]
        for chunk in chunks:
            client.send(chunk.encode("utf-8"))
            time.sleep(0.01)


def test_json_stream():
    server = threading.Thread(target=fake_gpsd_server)
    server.start()

    client = GPSDClient()
    for i, row in enumerate(client.json_stream()):
        print(row)


def test_json_stream2():
    server = threading.Thread(target=fake_gpsd_server)
    server.start()

    client = GPSDClient()
    for i, row in enumerate(client.json_stream()):
        print(row)
