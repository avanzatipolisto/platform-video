
import datetime
import re
def formatear_fecha(cadena:datetime)->str:
    """
    Pone un fecha en este formato: dd/mm/aaaa

    Argumentos:
        cadena (string)

    """
    cadena=cadena.strftime("%d/%m/%Y")
    return cadena







def formatear_cadena(cadena:str)->str:
    """
    Recorta un string a 10 caracters y si es menor lo rellena con espacios

    Argumentos:
        cadena (string)

    """
    #print("La longitud inicial de la cadena es: "+str(len(cadena)))
    cadena=cadena.strip()
    if len(cadena)>10:
        return cadena[:10]
    elif len(cadena)<10:
        return cadena+" "*(10-len(cadena))
    return cadena
def formatear_float(flotante:float)->str:
    """
    Pone 4 espacios a la derecha de un float o menos si el float tiene menos de 4 dígitos

    Argumentos:
        flotante (float)
    """
    texto_formateado =str(flotante)
    for i in range(4-len(texto_formateado)):
        texto_formateado = " "+texto_formateado
    return texto_formateado
def formatear_entero(entero:int)->str:
    """
    Pone 4 espacios a la izquierda de un entero o menos si el entero tiene menos de 4 dígitos

    Argumentos:
        entero (int)
    """
    texto_formateado =str(entero)
    for i in range(4-len(texto_formateado)):
        texto_formateado = texto_formateado+" "
    return texto_formateado
def check_empty(cadena):
    """
    Comprueba si una cadena esta vacia

    Argumentos:
        cadena (string)

    """
    cadena=cadena.strip()
    if len(cadena)==0 or not cadena:
        return True
    return False
    #raise ValueError("No puede estar vacio")
def is_greater_cero(number:int):
    """
    Coprueba si el número de páginas es mayor que 0

    Argumentos:
        number (entero)
    """
    if number>0: 
        return True
    return False
        #raise ValueError("El número de páginas no puede ser 0 o negativo")
def is_integer(numero:str):
    """
    Comprueba si el número es entero

    Argumentos:
        numero (string)
    """
    if not numero.isdigit():
        return False
    return True
def check_dni(dni):
    """
    Comprueba que el dni tiene el formato correcto y lo chequea con la letra correspondiente
    Args:
        dni (str): dni a comprobar

    Returns:
        bool: True si el dni es correcto, False en caso contrario
    """
    esCorrecto=False
    if(len(dni)!=9):
        return False
    letra= dni[8]
    letra=letra.upper()
    numeros_dni_string= dni[0:8]
    #print(numeros_dni)
    if (not numeros_dni_string.isdigit()):
        return False
    resto= int(numeros_dni_string)%23
    letras=["T","R","W","A","G","M","Y","F","P","D","X","B","N","J","Z","S","Q","V","H","L","C","K","E"]
    if letras[resto] == dni[8].upper():
        return True
    else:
        return False
def check_fecha(fecha):
    """
    Comprueba que la fecha tiene el formato correcto
    Args:
        fecha (str): fecha a comprobar

    Returns:
        bool: True si la fecha es correcta, False en caso contrario
    """
 
    formato = "%d-%m-%Y"  # Formato esperado: dd-mm-aaaa
    try:
        datetime.datetime.strptime(fecha, formato)
        return True  # Si no hay error, la fecha es válida
    except ValueError:
        return False  # Si hay un error, la fecha no es válida
def check_email(correo):
    """
    Comprueba que el correo tiene el formato correcto
    Args:
        correo (str): correo a comprobar

    Returns:
        bool: True si el correo es correcto, False en caso contrario
    """
    if "@" in correo and "." in correo:
        return True
    return False
def is_float(n):
    if isinstance(n, float):
        return True
    return False
def es_moneda_euros(cadena):
    """
    Comprueba si un string tiene el formato de una moneda de euros.

    Formatos válidos:
    - Cantidades con coma como separador decimal (opcionalmente con separador de miles).
    - El símbolo € puede ir al final (con o sin espacio) o al principio.
    - Ejemplos válidos: '123,45 €', '1.234,56 €', '€ 10', '0,99 €'.

    Args:
        cadena (str): El string a comprobar.

    Returns:
        bool: True si el string tiene el formato de moneda de euros, False en caso contrario.
    """
    # Expresión regular para validar monedas en euros
    patron = r"^\s?(\d{1,3}(\.\d{3})*|\d+)(,\d{2})?\s?$"
    
    # Comprobar si la cadena cumple el patrón
    resultado=bool(re.match(patron, cadena))
    return resultado
def float_moneda_a_str(float):
    """
    Convierte un float con formato de moneda en euros a un número float.

    Args:
        cadena (str): El string que representa la moneda (por ejemplo, '1.234,56').

    Returns:
        float: El valor numérico de la moneda como float.
        None: Si el formato no es válido.
    """
    try:
        cadena = str(float)
    except ValueError:
        return None
    #cadena_limpia = cadena.replace("€", "").replace(" ", "")
    cadena = cadena.replace(".", ",")
    # Convertir a float
    return cadena
def generar_letrar_dni(dni_sin_letra):
    letras=["T","R","W","A","G","M","Y","F","P","D","X","B","N","J","Z","S","Q","V","H","L","C","K","E"]
    letra_posición=int(dni_sin_letra)%23
    letra=letras[letra_posición]
    return letra