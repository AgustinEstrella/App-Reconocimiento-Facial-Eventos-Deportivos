from database import *
from config import MODELO_RECONOCIMIENTO

import numpy as np
import cv2
import face_recognition

def reconocimiento_facial():
    camara = cv2.VideoCapture(0) # Abre la primera cam que encuentra
    print("Iniciando cámara... Presiona 'q' para salir")

    vector_detectado = None # Creamos una variable para guardar el vector

    while True:
        ret, frame = camara.read()

        if not ret:
            print("Error en la camara")
            break

        # Convert the image from BGR color to RGB color
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Procesar rostro detectado en la camara
        for (top, right, bottom, left), rostro_actual_vector in zip(face_locations, face_encodings):
            # Escalar las coordenadas de vuelta al tamaño original de la cámara
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            vector_detectado = rostro_actual_vector

        cv2.imshow("Escaneando Rostro", frame)

        if vector_detectado is not None or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    camara.release()
    cv2.destroyAllWindows()

    return vector_detectado


def ingreso_usuario():
    #Ingreso DNI
    while True:
        dni = input("Ingrese su DNI (8 números): ")
        # Lo pasamos como String por validación octal
        # Se verifica que no tenga letras con isdigit
        if dni.isdigit() and len(dni) == 8 and "00000001" <= dni <= "72000000":

            if verificacion_usuario_existente(dni):
                print("Error: Ya se encuentra registrado el DNI ingresado")
            else:
                break

        else:
            print("Error: Solo ingrese 8 numeros validos entre 00000001 y 72000000")

    #Ingreso nombre
    while True:
            nombre = input("Ingrese su nombre, max 15 caracteres: ").strip()

            #Verificamos longitud y juntamos nombres compuestos
            if 1 <= len(nombre) <= 15 and nombre.replace(" ", "").isalpha():
                nombre = nombre.title() #Formatea primera letra a mayus
                break

            print("Error: Intente nuevamente")

    #Ingreso apellido
    while True:
        apellido = input("Ingrese su apellido, max 15 caracteres: ").strip()

        #Verificamos longitud y juntamos nombres compuestos
        if 1 <= len(apellido) <= 15 and apellido.replace(" ", "").isalpha():
            apellido = apellido.title() #Formatea primera letra a mayus
            break

        print("Error: Intente nuevamente")

    return dni, nombre, apellido

def buscar_usuario_biometricamente():
    vector = reconocimiento_facial()
    if vector is None:
        return

    resultado = buscar_usuario(vector)

    if resultado:
        dni, nombre, apellido, distancia = resultado

        print(f"Distancia: {distancia:.4f}")

        if distancia < 0.60: #0.60 de umbral es recomendado en la documentación de face_recognition
            print(f"Usuario encontrado!: Eres {nombre} {apellido} y tu DNI es {dni}")
        else:
            print("El rostro no coincide con ningun usuario registrado")
    else:
        print("No hay usuarios con rostros registrados")