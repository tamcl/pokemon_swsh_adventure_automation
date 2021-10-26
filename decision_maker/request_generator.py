import socket

host = '192.168.1.129'
port = 8888

obj = socket.socket()
obj.connect((host,port))
message = 'A 0.1s\n 0.1s'
message='quit_v'
obj.send(message.encode())
data = obj.recv(1024).decode()
print(data)
obj.close()