import socket
s = socket.socket()
s.connect(("localhost", 9993))
seguir = True
notEmail = True
while seguir:
    print(s.recv(1024).decode())
    s.send(input(": ").encode())
s.close()