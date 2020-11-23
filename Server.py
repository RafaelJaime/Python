"""
version 1.0.1
control if exist active user
"""

from threading import Thread, Lock
import socket

# you can write registered users file
def writeUsers(user,file):
    file = open(file, "a")
    file.write(user + "\n")
    file.close()

# you can read registered users file o Users Actives if
# exits return true
def readUsers(user, file):
    cont = 0
    with open(file, 'r') as f:
        for linea in f:
            if user in linea:
                cont += 1
        if cont > 0:
            return True

# you can write registered user in active users
def activeUsers(user, file):
    # we can read if user is active
    if not readUsers(user, file):
        file = open(file, "a")
        file.write(user + "\n")
        file.close()
    else:
        return "si existe"

    # you can delete active user


def deleteActiveUsers(user, file):
    f = open(file, "r")
    output = []
    for line in f:
        if not user in line:
            output.append(line)
    f.close()
    # open again the file and write all
    f = open(file, 'w')
    f.writelines(output)
    f.close()


class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente, codigo_cliente):
        Thread.__init__(self)
        self.socket = socket_cliente
        self.datos = datos_cliente
        self.codigo = codigo_cliente

    def run(self):
        # variables
        fActive = "activeUsers.txt"
        fRegist = "registeredUsers.txt"
        seguir = True
        mutex = Lock()
        while seguir:
            user = self.socket.recv(1000).decode()
            self.socket.send("hello, welcome to the server".encode())

            # send user if exist in user file
            mutex.acquire()
            isregist = readUsers(user, fRegist)
            mutex.release()

            if isregist:
                mutex.acquire()
                isActive = readUsers(user, fActive)
                mutex.release()
                if isActive:
                    self.socket.send("Your User was registered\n and your User was active ".encode())
                else:
                    print("estaba registrado no activo")
                    #user was registered and now we active
                    mutex.acquire()
                    activeUsers(user,fActive)
                    mutex.release()
                    self.socket.send("Your User was registered\n and now your User is active ".encode())
            #if user is not registered
            else:
                mutex.acquire()
                writeUsers(user,fRegist)
                mutex.release()
                mutex.acquire()
                activeUsers(user,fActive)
                mutex.release()
                self.socket.send("your user has been registered and is now active".encode())
            seguir=False
            self.socket.send("adios".encode())
         

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9993))
server.listen(1)
codigo_cliente = 1
# bucle para atender clientes
while 1:
    # Se espera a un cliente
    socket_cliente, datos_cliente = server.accept()
    # Se escribe su informacion
    print("conectado " + str(datos_cliente))
    hilo = Cliente(socket_cliente, datos_cliente, codigo_cliente)
    hilo.start()
    codigo_cliente += 1
