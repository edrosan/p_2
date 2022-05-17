
import datetime
import math


def crear_archivo(usuario, tabla_archivos, memoria, comando, memoria_disponible, tam_bloque):
    """
    Crea el archivo en memoria.

    Formato del comando:
        cat [nombre archivo] [tamaño a usar] [permisos]
    """
    nombre_archivo = comando[1]
    tam_archivo = int(comando[2])
    permisos = comando[3]
    id = 0
    if espacio_memoria (memoria_disponible, tam_archivo):
        bloques_archivo = bloques_usados(tam_bloque, tam_archivo)
        archivo = archivo_nuevo (nombre_archivo, tam_archivo, bloques_archivo, usuario, permisos)
        tabla_archivos.append(archivo)
        memoria = add_memoria (memoria, archivo, tam_bloque)
        memoria_disponible = actualizar_espacio(memoria)
        id = archivo['id']
    else:
        print("No hay espacio disponible")
    
    return (memoria, tabla_archivos, memoria_disponible, id)

def espacio_memoria (espacio_disponible, tam_archivo):
    """
    Verifica si hay espacio suficiente en memoria para
    crear un nuevo archivo.

    Devuelve True si hay espacio suficiente y False si
    no hay espacio suficiente.
    """
    if int(espacio_disponible) >= int(tam_archivo):
        return True
    else:
        return False

def bloques_usados (tam_bloque=1.0, tam_archivo=1.0):
    """
    Calcula los bloques que ocupara el archivo en memoria.

    Parametros:
            tam_bloque  --  Cantidad de bytes que un bloque puede almacenar.
            tam_archivo --  Tamaño en bytes que ocupa el archivo.

    """
    bloques_usados = math.ceil(tam_archivo / tam_bloque)
    print(f"Bloques usados: {bloques_usados}")
    return bloques_usados

def archivo_nuevo (nombre, tam_archivo, bloques_usados, usuario, permisos):
    """
    Da el formato necesario para guardar el archivo en memoria.
    """
    propietario = usuario
    time = datetime.datetime.now()
    id = nombre.upper()[0] +'-'+ str(time.hour) + str(time.minute) + str(time.second)
    time = time.strftime("%X")

    archivo = {
        'file':nombre, 
        'id':id, 
        'hora_creacion':time, 
        'file_size':tam_archivo,
        'propietario':propietario, 
        'permisos':permisos,  
        'bloques_usados':bloques_usados
        }

    return archivo

def add_memoria (memoria, archivo, tam_bloque):
    """
    Agrega el archivo a la memoria.
    """
    memoria_aux = memoria
    no_bloques = 0
    total_bytes = archivo['file_size']

    if archivo['bloques_usados'] == 1:
        iniciales = total_bytes
        final = iniciales
    else:
        iniciales = tam_bloque
        final = archivo['file_size'] - ((archivo['file_size']//tam_bloque*tam_bloque))
        if final == 0:
            final = iniciales

    for (indice, nodo) in enumerate(memoria):
        if nodo['id_file'] == 0:
            if no_bloques <= (archivo['bloques_usados'] - 1):
                size = nodo['size']
                if no_bloques == archivo['bloques_usados'] - 1:
                    memoria_aux[indice] = {'id_file': archivo['id'], 'no_parte': no_bloques, 'ocupado': final, 'size':size}
                else:
                    memoria_aux[indice] = {'id_file': archivo['id'], 'no_parte': no_bloques, 'ocupado': iniciales, 'size':size}
                no_bloques += 1
            else:
                return memoria_aux
    return memoria_aux

def actualizar_espacio(memoria):

    espacio_disponible = 0
    for file in memoria:
        if file['id_file'] == 0:
            espacio_disponible += file['size']

    espacio_disponible

    return espacio_disponible


def agregar_archivos_memoria(tabla_archivos, memoria, tam_bloque):
    for archivo in tabla_archivos:
        add_memoria (memoria, archivo, tam_bloque)
    
    return memoria


def eliminar_file(memoria, tabla_file, id):

    for file in tabla_file:
        if(file['id'] == id):
            tabla_file.remove(file)

    for (indice, file) in enumerate(memoria):
        size = file['size']
        if(file['id_file'] == id):
            memoria[indice] = {'id_file': 0, 'no_parte': 0, 'ocupado': 0, 'size':size}
            
    return (memoria, tabla_file)