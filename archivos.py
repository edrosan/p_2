

def info_archivo(archivo, path):
    id = ""
    permisos = ""
    propietario = ""
    File = open(path+archivo, "r")
    for line in File:
        line = line.replace("\n", "").split(":")
        if line[0] == 'id':
            id = line[1]
        if line[0] == 'permisos':
            permisos = line[1]
        if line[0] == 'propietario':
            propietario = line[1]
    File.close()
    
    return id, permisos, propietario

def permiso(permisos):
    permisos = list(permisos)
    propietario = tipo_permiso(int(permisos[0]))
    grupo = tipo_permiso(int(permisos[1]))
    otros = tipo_permiso(int(permisos[2]))

    return propietario, grupo, otros

def tipo_permiso(permiso):
    usuario = ""
    if permiso == 0:
        usuario = ""
    elif permiso == 1:
        usuario = "x"
    elif permiso == 2:
        usuario = "w"
    elif permiso == 3:
        usuario = "wx"
    elif permiso == 4:
        usuario = "r"
    elif permiso == 5:
        usuario = "rx"
    elif permiso == 6:
        usuario = "rw"
    elif permiso == 7:
        usuario = "rwx"
    return usuario