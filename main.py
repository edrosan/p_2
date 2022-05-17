
import subprocess
import os
import getpass
from ed_mem import *


from configuracion import *
from usuarios import *
from SO import iniciar

tam_memoria = 0
tam_bloque = 0
memoria_disponible = 0


(tam_memoria, tam_bloque, memoria_disponible) = importar_configuracion()
(total_bloques, tam_ultimo_bloque) = cant_bloques(tam_memoria, tam_bloque)

memoria = [ {'id_file':0, 'no_parte':0, 'ocupado':0, 'size':tam_bloque, 'permisos':777} ] * total_bloques

memoria[-1] = {
    'id_file':0, 
    'no_parte':0, 
    'ocupado':0, 
    'size':tam_ultimo_bloque,
    'permisos':777
    }

tabla_archivos = importar_archivos()
memoria = agregar_archivos_memoria(tabla_archivos, memoria, tam_bloque)

run = True

while(run):
    print()
    print("1.Ingresar")
    print("2.Nuevo usuario")
    print("3.Usuarios")
    print("4.Salir")

    try:
        opcion = int(input("Ingresa una opcion: "))
    except ValueError:
        opcion = 0
# ----------------------------------------------------------------
    if opcion == 1:
        print()
        print("Ingresar al sistema")
        usuario = input("Usuario: ")
        passw = getpass.getpass('Contraseña:')

        if autenticar(usuario, passw):
            path = f"./S/{usuario}/"

            iniciar(path, usuario, memoria_disponible, memoria, tabla_archivos, tam_bloque)
        else:
            print("Error de validacion de credenciales.")
# ----------------------------------------------------------------
    elif opcion == 2:
        print()
        print("Crear nuevo usuario:")
        crear_usuario()
    elif opcion == 3:
        print()
        print("Usuarios:")
        ver_usuarios()
    elif opcion == 4:
        run = False
    else:
        print("Opcion no valida")