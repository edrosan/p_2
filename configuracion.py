
import math
import ast

def importar_configuracion():
    """
    Importa la configuracion del sistema.

    Devuelve el tamaño de la memoria, el tamaño
    del los bloques y la memoria disponible.

    Excepciones:
    FileNotFoundError -- Si el archivo de configuracion 
    del sistema no se encuetra en la carpeta.
    
    """
    File = open("./conf.log", "r")
    for line in File:
        line = line.replace("\n", "").split(":")
        if line[0] == "mem":
            ram = int(line[1])
        if line[0] == "bloq":
            tam_bloq = int(line[1])
        if line[0] == "libre":
            memoria_disponible = int(line[1])
    File.close()

    return (ram, tam_bloq, memoria_disponible)

def guardar_archivos(tabla):
    File = open("./mem.log", "w")
    for archivo in tabla:
        File.write(str(archivo)+"\n")
    
    File.close()

def guardar_conf(memoria_libre):
    File = open("./conf.log", "w")
    File.write("mem:64\n")
    File.write(f"libre:{memoria_libre}\n")
    File.write("bloq:3\n")
    File.close()


def importar_archivos():
    """
    Carga los archivos.
    """
    tabla = []
    File = open("./mem.log", "r")
    for line in File:
        tabla.append(ast.literal_eval(line))
    File.close()

    return tabla

def cant_bloques(tam_memoria, tam_bloques):
    """
    Calcula la cantidad de bloques que podra tener la memoria RAM.

    Dependiendo del tamaño del bloque, el ultimo bloque puede tener
    diferente tamaño.

    Devuelve el total de bloques que puede tener la RAM y el tamaño del 
    ultimo bloque.

    Parametros:
        tam_memoria -- tamaño de la memoria RAM.\n
        tam_bloques -- tamaño de los bloques.
    
    Excepciones:
        ZeroDivisionError -- Si el tamaño de bloques es 0 no se puede efecturar la división.
    """

    total_bloques = math.ceil(tam_memoria/tam_bloques)
    ultimo_bloque =  tam_memoria - (tam_memoria//tam_bloques)*tam_bloques

    if ultimo_bloque == 0:
        ultimo_bloque = tam_bloques

    return (total_bloques, ultimo_bloque)

def agregar_memoria():
    File = open("./archivos.log", "r")
    for line in File:
        line = line.replace("\n", "").split(":")
        if line[0] == "mem":
            ram = line[1]
        if line[0] == "bloq":
            tam_bloq = line[1]
    File.close()