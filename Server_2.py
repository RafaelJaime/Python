import threading
from threading import Thread
import socket

"""
user para guardar el correo del usuario
"""

# Read and write new group
Fgrupos = "archivos/grupos.txt"
mutexGrupos = threading.Lock()

# Metodo que recibe el nombre del grupo y sus 3 usuarios, devuelve true si lo crea y false si ya existe
def newGroup(name, usuario1, usuario2, usuario3):
    global Fgrupos, mutexGrupos
    cont = 0
    with open(Fgrupos, "r+") as f:
        for linea in f:
            if name in linea:
                cont +=1
        if cont>0:
            return False
        else:
            file = open(Fgrupos, "a")
            file.write(name +  ";" + usuario1 +  ";" + usuario2 +  ";" + usuario3)
            return True



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
        global menclient
        mutex = threading.Lock()

        while (seguir!=True):
            menclient = self.socket.recv(1000).decode()

            if(menclient=="I"):


                self.socket.send("hello, welcome to the server\nenter your email".encode())


                user = self.socket.recv(1000).decode()

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
                        #self.socket.send("adios")
                    else:
                        print("estaba registrado no activo")
                        # user was registered and now we active
                        mutex.acquire()
                        activeUsers(user, fActive)
                        mutex.release()
                        self.socket.send("Your User was registered\n and now your User is active ".encode())
                        #self.socket.send("adios")
                # if user is not registered
                else:
                    mutex.acquire()
                    writeUsers(user, fRegist)
                    mutex.release()
                    mutex.acquire()
                    activeUsers(user, fActive)
                    mutex.release()
                    self.socket.send("your user has been registered and is now active".encode())
                    #self.socket.send("adios")
                    menclient=""



            if(menclient=="O"):

                '''
                    no tengo controlado que se ponga antes O que I
                if len(user)==0:
                    print("no hay")
                    self.socket.send("no hay user")
                '''
                mutex.acquire()
                deleteActiveUsers(user,fActive)
                mutex.release()
                self.socket.send("your user is not now active".encode())

            if(menclient!="I" and menclient!="O"):
                self.socket.send("your menssage is not correct ".encode())
                print("no es ni I ni O")









server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9992))
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
