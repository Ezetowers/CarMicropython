import socket

s = socket.socket()
s.connect(('192.168.4.1', 54321))
s.send(b'EXIT')
s.close()
