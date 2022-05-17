

import os
import subprocess


def crear_usuario():

    if os.path.exists("usuarios.log"):
        File = open("./usuarios.log", "a")
        usuario = input("Nombre de usuario: ")
        passw = input("Contraseña: ")
        File.write(usuario+":"+passw+"\n")
        File.close()

        subprocess.run(["mkdir", usuario])
        subprocess.run(["mv", "./"+usuario, "./S/"])

    else:
        print("Error archivo corrupto")
    
def ver_usuarios():

    if os.path.exists("usuarios.log"):
        File = open("./usuarios.log", "r")
        for line in File: 
            print(line.split(":")[0])
        File.close()
    else:
        print("Error archivo corrupto")

def autenticar(usuario, passw):
    if os.path.exists("usuarios.log"):
        File = open("./usuarios.log", "r")
        for line in File: 
            if line.split(":")[0] == usuario and line.split(":")[1].replace('\n', "") == passw:
                return True
        File.close()
    else:
        print("Error archivo corrupto")
    
    return False