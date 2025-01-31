import os   
import datetime
import csv

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


def restore_csv_backup(archivo):
    filas={
        "usuarios":[],
        "contents":[],
        "users_contents":[]
    }
    fila_tipo=None
    try:
        with open(archivo, "r", encoding='utf-8') as f:
            reader = csv.reader(f)
            for linea,fila in enumerate(reader):   
                if (len(fila)==0 or fila==None):
                    continue         
                if fila[0]=="id" and fila[1]=="name":   
                    fila_tipo="users"
                    continue
                elif fila[0]=="id" and fila [1]=="type":
                    fila_tipo="contents"
                    continue
                elif fila[0]=="id" and fila[1]=="users_id":
                    fila_tipo="users_contents"
                    continue

                if fila_tipo=="users":
                    if len(fila) ==5: 
                        filas["users"].append(fila)
                elif fila_tipo=="contents":
                    if len(fila) ==6:  
                        filas["contents"].append(fila)   
                elif fila_tipo=="users_contents":
                    if len(fila) ==3:
                        filas["users_contents"].append(fila)
                

        return filas
    except Exception as e:  
        print("hubo un error al leer el archivo: ",e)
        return None
def write_csv_file(users, contents, users_contents):
    ahora = datetime.datetime.now()
    ahora = ahora.strftime("%Y%m%d%H%M%S")
    archivo_csv=str(ahora)+"_backup_agenda.csv"
    try:
        with open(archivo_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "password", "email", "birddate", "rol"])
            for fila in users:
                writer.writerow([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]])
            writer.writerow(["id", "type", "genre", "tile", "year", "image", "clicks"])
            for fila in contents:
                writer.writerow([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]])
            writer.writerow(["id", "user_id", "content_id"])
            for fila in users_contents:
                writer.writerow([fila[0], fila[1], fila[2]])
    except Exception as e:  
        print(e)