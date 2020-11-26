import socket



# Se establece la conexion
s = socket.socket()
# conexion al localhost y puerto
s.connect(("localhost", 9992))

seguir = True
notEmail = True
while seguir:
    '''while notEmail:
        menClient = input("enter your email :")
        if "@" in menClient:
            notEmail = False
    '''
    menClient = input("enter your menssage :")
    s.send(menClient.encode())
    menServer = s.recv(1024).decode()
    print(menServer)
    if ("adios" == menServer ):
        seguir = False

s.close()
