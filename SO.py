import os
import subprocess

from configuracion import *
from comandos import *
from ed_mem import *
from archivos import *

def iniciar(path, usuario, memoria_disponible, memoria, tabla_archivos, tam_bloque):
    subprocess.run(["clear"])
    print(f"----- Bienvenido {usuario} -----")
    while (True):
        usuario = usuario
        memoria_disponible = memoria_disponible
        comando = input(path+" -> ").split()
        if len(comando) == 0:
            comando.append("h")

        if comando[0] == "--h" or comando[0] == "--help":
            print("Comandos: help, info, cat, clear, ls, dir, mkdir, cd, pwd, rm, read, write, defrag, list exit")
# ----------------------------------------------------------------
# Informacion
        if comando[0] == "info" or comando[0] == "i":
            if len(comando) <= 1:
                info(usuario, memoria_disponible)

            elif comando[1] == "memoria" or comando[1] == "m":
                info_memoria(memoria, memoria_disponible)

            elif comando[1] == "archivos" or comando[1] == "a":
                info_archivos(tabla_archivos)
# -----------------------------------------------------------------------
# Crear archivo
        if comando[0] == "cat":
            
            if len(comando) > 3:

                if validar_permisos(comando[3]) and not(os.path.exists(f"{path}{comando[1]}"+".acu") ):
                    (memoria, tabla_archivos, memoria_disponible, id) = crear_archivo(usuario, tabla_archivos, memoria, comando, memoria_disponible, tam_bloque)
                    if id != 0:
                        cat(comando, path, id, usuario)
                    guardar_archivos(tabla_archivos)
                    guardar_conf(memoria_disponible)
                else:
                    print("Permisos no validos o archivo existente")

            elif comando[1] == "--h" or comando[1] == "--help":
                cat_help()
            else:
                print("Modo de uso: cat [nombre] [tamaño] [permisos 000-777]")

# -----------------------------------------------------------------------
# Limpiar pantalla
        if comando[0] == "clear":
            subprocess.run(["clear"])

# -----------------------------------------------------------------------
        if comando[0] == "ls" or comando[0] == "dir":
            subprocess.run(["ls", path])

# -----------------------------------------------------------------------
# Crear carpeta
        if comando[0] == "mkdir":
            if "./S/" in path:
                subprocess.run(["mkdir", comando[1]])
                subprocess.run(["mv", "./"+comando[1], path])
            else:
                print("No se pueden crear carpetas en esta ubicacion")
# -----------------------------------------------------------------------
# Cambiar de directorio
        if comando[0] == "cd":

            if os.path.exists(path+comando[1]) and os.path.isdir (path+comando[1]) and (comando[1]!= ".."):
                path += comando[1] + "/"
            elif not(os.path.exists(path+comando[1])):
                print("No exite el directorio")
            elif not(os.path.isdir (path+comando[1])):
                print("No es un directorio")
            elif comando[1]== ".." and len(path.split("/")) > 2:
                path_aux = path.split("/")
                path_aux.pop(-2)
                path = "/".join(path_aux)
# -----------------------------------------------------------------------
# Comando pwd
        if comando[0] == "pwd":
            print(path)
# ---------------------------------
        if comando[0] == "rm":
            if len(comando) == 2:

                if comando[1] == "--h" or comando[1] == "--help":
                    rm_help()
                else:
                    archivo = comando[1]+".acu"
                    if os.path.exists(path+archivo) and not(os.path.isdir(path+archivo)):
                        print(archivo)
                        id, permisos, propietario = info_archivo(archivo, path)
                        per_propietario, per_grupo, per_otros = permiso(permisos)


                        if usuario == propietario:
                            if "x" in per_propietario:
                                eliminado = not(subprocess.run(["rm", path+archivo]).returncode)
                                if eliminado:
                                    memoria, tabla_archivos = eliminar_file(memoria, tabla_archivos, id)
                                    guardar_archivos(tabla_archivos)
                                    memoria_disponible = actualizar_espacio(memoria)
                                    guardar_conf(memoria_disponible)
                                    print("Archivo eliminado.")
                            else:
                                print("No se tiene los permisos necesarios.")
                        else:
                            if "x" in per_otros:
                                eliminado = not(subprocess.run(["rm", path+archivo]).returncode)
                                if eliminado:
                                    memoria, tabla_archivos =  eliminar_file(memoria, tabla_archivos, id)
                                    guardar_archivos(tabla_archivos)
                                    memoria_disponible = actualizar_espacio(memoria)
                                    guardar_conf(memoria_disponible)
                                    print("Archivo eliminado.")
                            else: 
                                print("No se tiene los permisos necesarios.")
        
            elif len(comando) > 2:
                carpeta = comando[2]
                if "./S/" in path:
                    if os.path.exists(path+carpeta) and os.path.isdir(path+carpeta):
                        if len(os.listdir(path+carpeta)) != 0:
                            print("Borre los archivos dentro de la carpeta individualmente.")
                        else:
                            eliminado = not(subprocess.run(["rm", "-r", path+carpeta]).returncode)
                            if eliminado:
                                print("Se elimino correctamente el directorio.")
                    else:
                        print("No existe el directorio o no es un directorio.")
                else:
                    print("No se pueden eliminar carpetas del sistema")
        # ---------------------------------
        if comando[0] == "write" or comando[0] == "w":
            if permiso_edit(path, comando[1], usuario, "w"):
                if len(comando) < 3:
                    if write(path,comando[1]):
                        print("Se agrego el texto.")
                    else:
                        print("Error al añadir el texto")
# ---------------------------------
        if comando[0] == "read" or comando[0] == "r":
            if permiso_edit(path, comando[1], usuario, "r"):
                if len(comando) == 2:
                    read(path, comando[1])
                else: 
                    print(f"Forma de uso: read [nombre_archivo]")
# ---------------------------------
        if comando[0] == "defrag" or comando[0] == "def":
            memoria = desfragmentar(memoria, tabla_archivos, tam_bloque)
            memoria_disponible = actualizar_espacio(memoria)
            guardar_conf(memoria_disponible)
# ---------------------------------
        if comando[0] == "list":
            print()
            print("[ / ]-> "+lista("./"))
            print()

        if comando[0] == "exit":
            break
    
    return (memoria, tabla_archivos)