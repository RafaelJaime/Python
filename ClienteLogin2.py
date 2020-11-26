import socket



# Se establece la conexion
s = socket.socket()
# conexion al localhost y puerto
s.connect(("localhost", 9993))

seguir = True
notEmail = True
while seguir:
    print(s.recv(1024).decode())
    s.send(input(": ").encode())

s.close()
