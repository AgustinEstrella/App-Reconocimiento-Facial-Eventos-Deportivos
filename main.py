#App reconocimiento facial (CLI)
from unittest import case

from functions import *
from database import *

def menu():
    while True:
        print("1: Registrar usuario")
        print("2: Identificar usuario")
        print("3: Salir")
        opcion = input("Seleccione una opcion: ")

        match opcion:
            case "1":
                dni, nombre, apellido = ingreso_usuario()
                creacion_usuario(dni, nombre, apellido)
                datos_biometricos = reconocimiento_facial()
                adicion_rostro(datos_biometricos, dni)
            case "2":
                buscar_usuario_biometricamente()
            case "3":
                break

menu()