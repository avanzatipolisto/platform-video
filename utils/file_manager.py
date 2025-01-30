import os   



def copy_assets(origen, destino):
    if not os.path.exists(destino):
        os.makedirs(destino)  # Crear el directorio de destino si no existe

    for root, dirs, files in os.walk(origen):
        # Obtener la ruta relativa desde el directorio de origen
        relative_path = os.path.relpath(root, origen)
        destino_actual = os.path.join(destino, relative_path)

        if not os.path.exists(destino_actual):
            os.makedirs(destino_actual)  # Crear subdirectorios en destino

        for file in files:
            origen_archivo = os.path.join(root, file)
            destino_archivo = os.path.join(destino_actual, file)
            with open(origen_archivo, "rb") as f_origen:
                with open(destino_archivo, "wb") as f_destino:
                    f_destino.write(f_origen.read())  # Copiar archivo byte a byte

    print(f"El directorio '{origen}' se ha copiado exitosamente en '{destino}'.")


def delete_folder(directorio):
    if os.path.exists(directorio):
        for archivo in os.listdir(directorio):
            ruta_archivo = os.path.join(directorio, archivo)
            if os.path.isfile(ruta_archivo):  # Solo borra archivos
                os.remove(ruta_archivo)
        print(f"Archivos en '{directorio}' eliminados correctamente.")
    else:
        print(f"El directorio '{directorio}' no existe.")

def delete_file(file):
    if os.path.exists(file):
        os.remove(file)
    else:
        print(f"El archivo '{file}' no existe.")