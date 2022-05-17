
import datetime
import os
import re
import subprocess

from archivos import *
from ed_mem import *


def info(usuario, memoria_disponible):
    print()
    time = datetime.date.today()
    time = time.strftime("%A %d %B %Y")
    print(f"Usuario: {usuario}")
    print(f"Fecha: {time}")
    time = datetime.datetime.now()
    time = time.strftime("%X")
    print(f"Hora: {time}")
    print(f"Memoria disponible: {memoria_disponible} bytes")
    print("Version OS: 0.9.9")
    print()

def info_memoria(memoria, memoria_disponible):
    """
    Muestra informacion acerca del estado de la memoria.
    """
    print()
    print("---Inforacion de la memoria---")
    print(f"Espacio disponible en memoira: {memoria_disponible}")
    print("Memoria:")
    print("[", end="")
    for file in memoria:
        print(f"{file['id_file']}:{file['no_parte']}", end=" | ")
    print("]")
    print()

def info_archivos(tabla):
    print()
    print("Archivos en memoria")
    print("--"*50)
    b = '\x1b[48;5;231m'
    r = '\x1b[0m'
    print(f"|\tNombre\t|Hora Creacion\t|Tamaño en Bytes\t|Bloques usados\t|Propietario\t|Permisos  |")
    print("--"*50)
    for file in tabla:
        print(f"|\t  {file['file']}\t| {file['hora_creacion']}\t|    {file['file_size']}\t\t\t|  {file['bloques_usados']}\t        |  {file['propietario']}\t|  {file['permisos']}\t   |")
    print("--"*50)
    print()

def cat(comando, path, id, propietario):
    """
    Crea un archivo en la carpeta del usuario correspondiente.

    El archivo se guarda con la extension ".acu" (Archivo Creado por el Usuario).

    Ejemplo comando:
        -> cat [nombre archivo] [tamaño a usar] [permisos]

    Parametros:
        comando --  Comando que tiene toda la informacion para la
                    creacion del archivo nuevo.
        path    --  Direccion donde se creara el nuevo archivo.
    """
    nombre_archivo = comando[1]+".acu"
    tam_archivo = comando[2]
    permisos = comando[3]

    subprocess.run(["touch", nombre_archivo])

    File = open("./"+nombre_archivo, "a")
    File.write("id:"+id+"\n")
    File.write("propietario:"+propietario+"\n")
    File.write("tamaño:"+tam_archivo+"\n")
    File.write("permisos:"+permisos+"\n")
    File.write("...\n")
    File.close()

    subprocess.run(["mv", "./"+nombre_archivo, path])
    
def cat_help():
    """
    Muestra informacion de ayuda para el comando cat.

    Modo de uso: cat [nombre] [tamaño] [permisos 000-777]
    """
    print()
    print("Modo de uso: cat [nombre] [tamaño] [permisos 000-777]")
    print("\tnombre: Nombre del nuevo archivo.")
    print("\ttamaño: Tamaño en bytes que ocupara el nuevo archivo.")
    print("\tpermisos: Permisos para el archivo:")
    print("\t\t7-7-7")
    print("\t\trwx-rwx-rwx")
    print("\t\tpropietario-grupo-otros")
    print("\t\tr-w-x: lectura, escritura, ejecucion")
    print("\t\t0-0-0 = 0 -> Ningun permiso")
    print("\t\t0-0-1 = 1 -> Permiso de ejecucion")
    print("\t\t0-1-0 = 2 -> Permiso de escritura")
    print("\t\t0-1-1 = 3 -> Permiso de ejecucion")
    print("\t\t1-0-0 = 4 -> Permiso de lectura")
    print("\t\t1-0-1 = 5 -> Permiso de lectura y ejecucion")
    print("\t\t1-1-0 = 6 -> Permiso de lectura y escritura")
    print("\t\t1-1-1 = 7 -> Todos los permisos")
    print()

def rm_help():
    """
        Modo de uso, eliminar archivos:
            rm [nombre archivo]
        
        Modo de uso, eliminar directorio:
            rm -r [nombre directorio]
    """
    print("Modo de uso, eliminar archivos:")
    print("\trm [nombre archivo]")
    print()
    print("Modo de uso, eliminar directorio:")
    print("\trm -r [nombre directorio]")
    print()

def read(path, archivo):
    """
    Lee el contenido del archivo
    """
    datos = False
    archivo = path+archivo+".acu"
    if os.path.exists(archivo) and not(os.path.isdir(archivo)):
        File = open(archivo, "r")
        print()
        print("-------------Contenido-------------------")
        print()
        for line in File:
            line = line.replace("\n", "")
            if datos:
                print(f"\t{line}")
            if line == "...":
                datos = True
        File.close()
        print()
    else:
        print("No existe el archivo")

def write(path,archivo):
    """
    Añade texto un archivo.
    """
    archivo = path+archivo+".acu"
    if os.path.exists(archivo) and not(os.path.isdir(archivo)):
        File = open(archivo, "a")
        texto = input("Ingresa el texto: ")
        File.write(texto+"\n")
        File.close()
        return True
    return False

def permiso_edit(path, archivo, usuario, per):
    archivo = archivo+".acu"
    id, permisos, propietario = info_archivo(archivo, path)
    per_propietario, per_grupo, per_otros = permiso(permisos)
    if  not(os.path.exists(path+archivo)):
        print("No se encontro el archivo")
        return False
    if usuario == propietario:
        if per in per_propietario:
            return True
        else:
            print("No se tiene el permiso necesario")
            return False
    else:
        if per in per_otros:
            return True
        else:
            print("No se tiene el permiso necesario")
            return False


def permiso_lec(path, archivo, usuario):
    archivo = archivo+".acu"
    id, permisos, propietario = info_archivo(archivo, path)
    per_propietario, per_grupo, per_otros = permiso(permisos)
    if  not(os.path.exists(path+archivo)):
        print("No se encontro el archivo")
        return False
    if usuario == propietario:
        if "r" in per_propietario:
            return True
        else:
            print("No se tiene el permiso necesario")
            return False
    else:
        if "r" in per_otros:
            return True
        else:
            print("No se tiene el permiso necesario")
            return False

def validar_permisos(permisos):
    permisos = list(permisos)
    if len(permisos) == 3:
        if int(permisos[0]) >= 0 and int(permisos[0]) <= 7:
            if int(permisos[1]) >= 0 and int(permisos[1]) <= 7:
                if int(permisos[2]) >= 0 and int(permisos[2]) <= 7:
                    return True
    return False


def desfragmentar(memoria, tabla_file, tam_bloque):
    memoria_aux = memoria
    file_critico = memoria[-1]['id_file']

    for (indice,file) in enumerate(memoria):
        size = file['size']
        memoria_aux[indice] = {'id_file': 0, 'no_parte': 0, 'ocupado': 0, 'size':size}

    for file in tabla_file:
        if file['id'] != file_critico:
            add_memoria (memoria, file, tam_bloque)

    for file in tabla_file:
        if file['id'] == file_critico:
            add_memoria (memoria, file, tam_bloque)

    return memoria_aux


# ./
tab = 1
def lista(path):
    global tab
    l = ""
    lista_archivos = os.listdir(path)
    
    l+="\n"
    for i in range(0, tab):
        l+=("   ")
    for archivo in lista_archivos:
        if os.path.isdir(path+archivo):
            tab+=1
            l+= "["+archivo+"]"
            l+=("->")
            l+=(lista(path+archivo+"/", ))
            tab -= 1
            l+=("\n")
            for i in range(0, tab):
                l+=("   ")
        else:
            l+= archivo
            l+=("\n")
            for i in range(0, tab):
                l+=("   ")
    return l