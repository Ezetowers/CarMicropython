import socket
import time
s = socket.socket()
s.connect(('192.168.4.1', 54321))
s.send(b'FORWARD|ACCELERATE|ACCELERATE|ACCELERATE|ACCELERATE|ACCELERATE')
time.sleep(10)
s.close()
