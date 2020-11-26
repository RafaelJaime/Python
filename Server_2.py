import threading
from threading import Thread
import socket
import random

# Read and write new group
Factive = "archivos/activeUsers.txt"
Fregist = "archivos/registeredUsers.txt"
Fgroups = "archivos/grupos.txt"
Ftest = "archivos/test.txt"
mutexGroups = threading.Lock()
mutexRegist = threading.Lock()
mutexActive = threading.Lock()
mutexTest = threading.Lock()

# Metodo que recibe el nombre del grupo y sus 3 usuarios, devuelve true si lo crea y false si ya existe
def newGroup(name, usuario1, usuario2, usuario3):
    global Fgroups, Factive, groupName
    cont = 0
    groupName = name + ";" + usuario1 + ";" + usuario2 + ";" + usuario3
    with open(Fgroups, "r+") as f:
        for linea in f:
            if groupName in linea:
                cont += 1
        if cont > 0:
            return False
        else:
            mutexActive.acquire()
            if(readUsers(usuario1, Factive) and readUsers(usuario2, Factive) and readUsers(usuario3, Factive)):
                file = open(Fgroups, "a")
                file.write(groupName + "\n")
                mutexActive.release()
                return True
            else:
                return False


# you can write registered users file
def writeUsers(user, file):
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
        global Fregist, Factive
        seguir = False
        acceder = False
        user = ""
        message = ""
        # Comprobar si el usuario esta registrado
        while(seguir != True):
            while(user.find('@') == -1):
                self.socket.send(message.encode() +
                                 "\nEnter correct email with @ ".encode())
                user = self.socket.recv(1000).decode()
            mutexRegist.acquire()
            isregist = readUsers(user, Fregist)
            mutexRegist.release()
            if isregist:
                mutexActive.acquire()
                isActive = readUsers(user, Factive)
                mutexActive.release()
                if isActive:
                    message = "Your User was registered and is currently active, please select other name."
                    user = ""
                else:
                    mutexActive.acquire()
                    activeUsers(user, Factive)
                    mutexActive.release()
                    message = "Your User was registered and and now is active."
                    seguir = True
            else:
                mutexRegist.acquire()
                writeUsers(user, Fregist)
                mutexRegist.release()
                mutexActive.acquire()
                activeUsers(user, Factive)
                mutexActive.release()
                message = "Your user has been registered and is now active"
                seguir = True

        print("Nuevo usuario en el sistema:  " + user)
        while(acceder != True):
            answer = 0
            while(answer > 3 or answer < 1 or answer == ""):
                self.socket.send(message.encode() +
                                 "\nWrite: \n\t1.- View competitions\n\t2.- Create a group\n\t3.-Logout".encode())
                message = ""
                answer = int(self.socket.recv(1000).decode())
            if(answer == 1):
                print("Esta viendo competiciones")
            elif (answer == 2):
                self.socket.send("Write the name of the group: ".encode())
                groupName = self.socket.recv(1000).decode()
                self.socket.send(
                    "Write the name of a member of the group: ".encode())
                user2 = self.socket.recv(1000).decode()
                self.socket.send(
                    "Write the name of the last member of the group: ".encode())
                user3 = self.socket.recv(1000).decode()
                mutexGroups.acquire()
                if(newGroup(groupName, user, user2, user3)):
                    ready = False
                    mutexGroups.release()
                    while(ready != True):
                        self.socket.send(
                            "Ready to start with the test (yes or not): ".encode())
                        answer = self.socket.recv(1000).decode()
                        if answer == "yes":
                            ready = True
                    global Ftest, mutexTest
                    respuestas = []
                    pregunta = 1
                    cont = 1
                    cont2 = 1
                    puntuacion = 0.0
                    with open(Ftest, "r+") as f:
                        for linea in f:
                            if(pregunta == 1 or pregunta == 5 or pregunta == 9 or pregunta == 13 or pregunta == 17 or pregunta == 21 or pregunta == 25 or pregunta == 29 or pregunta == 33 or pregunta == 37):
                                respuestas = []
                                linea = linea.replace('*', '')
                                mensaje = "----------------------------\n" + linea + "\n"
                            else:
                                linea = linea.replace('+', '')
                                respuestas.append(linea)
                                if(pregunta == 2 or pregunta == 6 or pregunta == 10 or pregunta == 14 or pregunta == 18 or pregunta == 22 or pregunta == 26 or pregunta == 30 or pregunta == 34 or pregunta == 38):
                                    correcta = linea
                                cont += 1
                                if(cont > 3):
                                    random.shuffle(respuestas)
                                    mensaje += str(1)+") " + respuestas[0] + "\n" + str(
                                        2)+") " + respuestas[1] + "\n" + str(3)+") " + respuestas[2] + "\n"
                                    for i in range(3):
                                        cont2 += 1
                                    if(cont2 > 3):
                                        opcion = 0
                                        while(opcion < 1 or opcion > 3):
                                            mensaje += "Choose one, 1, 2 o 3: "
                                            self.socket.send(mensaje.encode())
                                            opcion = int(
                                                self.socket.recv(1000).decode())
                                        if(opcion == 1):
                                            if(respuestas[0] == correcta):
                                                puntuacion += 1
                                            else:
                                                puntuacion -= 0.2
                                        elif(opcion == 2):
                                            if(respuestas[1] == correcta):
                                                puntuacion += 1
                                            else:
                                                puntuacion -= 0.2
                                        elif(opcion == 3):
                                            if(respuestas[2] == correcta):
                                                puntuacion += 1
                                            else:
                                                puntuacion -= 0.2
                                        cont2 = 1
                                    cont = 1
                            pregunta += 1
                    self.socket.send(
                        ("Has obtenido " + str(puntuacion)+" puntos").encode())
                    mutexGroups.acquire()
                    f = open(Fgroups, "r")
                    output = []
                    for line in f:
                        if not groupName in line:
                            output.append(line)
                    f.close()
                    f = open(Fgroups, 'w')
                    f.writelines(output)
                    f.close()
                    mutexGroups.release()

                else:
                    self.socket.send("Your group is wrong".encode())
            elif (answer == 3):
                mutexActive.acquire()
                deleteActiveUsers(user, Factive)
                mutexActive.release()
                self.socket.send("your user is not now active".encode())
                self.socket.close()
                break


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9993))
server.listen(1)
codigo_cliente = 1
if __name__ == '__main__':
    while 1:
        socket_cliente, datos_cliente = server.accept()
        print("conectado " + str(datos_cliente))
        hilo = Cliente(socket_cliente, datos_cliente, codigo_cliente)
        hilo.start()
        codigo_cliente += 1
