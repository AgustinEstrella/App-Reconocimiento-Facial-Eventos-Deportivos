from database import *
from config import MODELO_RECONOCIMIENTO

import numpy as np
import cv2
from deepface import DeepFace

def reconocimiento_facial():
    camara = cv2.VideoCapture(0) #Abre la primera cam que encuentra
    print("Mira fijamente a la camara y presiona la tecla 's' para realizar el escaneo")

    vector_numerico = None

    while True:
        ret, frame = camara.read()
        if not ret:
            print("Error: no se pudo leer la camara")
            break

        cv2.imshow("Captura facial", frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord('s'):
            print("Procesando rostro")
            try:
                resultado = DeepFace.represent(
                    img_path = frame,
                    model_name = MODELO_RECONOCIMIENTO,
                    enforce_detection = True,
                    detector_backend = "mtcnn")[0]

                vector_numerico = resultado["embedding"] #Conseguimos el vector facial
                vector_numerico = np.array(vector_numerico, dtype=np.float32)
                vector_numerico = vector_numerico / np.linalg.norm(vector_numerico)

                area_facial = resultado["facial_area"]

                print("Rostro escaneado correctamente!")

            except Exception as e:
                print(f"Error al reconocer, {e} verifica condiciones lumínicas y no te muevas")
        elif tecla == ord('q'):
            break

    camara.release()
    cv2.destroyAllWindows()

    return vector_numerico

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

        if distancia < 0.30:
            print(f"Usuario encontrado!: Eres {nombre} {apellido} y tu DNI es {dni}")
        else:
            print("El rostro no coincide con ningun usuario registrado")
    else:
        print("No hay usuarios con rostros registrados")