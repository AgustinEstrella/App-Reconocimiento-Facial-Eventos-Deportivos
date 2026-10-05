#App reconocimiento facial (CLI)
from unittest import case

import cv2
from deepface import DeepFace

from functions import ingreso_usuario

def menu():
    while True:
        print("1: Registrar usuario")
        print("2: Identificar usuario")
        print("3: Salir")
        opcion = input("Seleccione una opcion")

        match opcion:
            case "1":
                dni, nombre, apellido = ingreso_usuario()



