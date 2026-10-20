from database import *

import re #usamos regex para la validacion de correo electronico

import time
import cv2
import face_recognition


#Registros
def registro_dni():
    # Ingreso DNI
    while True:
        dni = input("Ingrese su DNI (8 números): ").strip()

        if dni.isdigit() and len(dni) == 8 and "00000001" <= dni <= "72000000":
            if verificacion_usuario_existente(dni):
                print("Error: Ya se encuentra registrado el DNI ingresado")
            else:
                break
        else:
            print("Error: Solo ingrese 8 numeros validos entre 00000001 y 72000000")


    return dni

def registro_contrasenia():
    while True:
        contrasenia = input("Ingrese la contraseña para su cuenta."
                            "Minimo 8 caracteres, incluida 1 mayus"
                            "1 minus y un caracter especial: ").strip()

        if validar_contrasenia(contrasenia):
            break

        print("Error al ingresar la contraseña, revisa los requerimientos")

    return contrasenia

def validar_correo(correo):
    patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if re.match(patron, correo):
        return True
    else:
        return False

def validar_contrasenia(texto):
    #Pedimos 1 mayus, 1 minus, 1 caracter especial y 8 caracteres minimos
    requisito_contraseña = re.compile(r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$')

    if re.match(requisito_contraseña, texto):
        return True
    else:
        return False

def registro_usuario():

    dni = registro_dni()

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

    #Ingreso email
    while True:
        email = input("Ingrese su email: ").strip()

        if validar_correo(email):
            break

        print("Revise el correo e intente nuevamente")


    contrasenia = registro_contrasenia()

    return dni, nombre, apellido, email, contrasenia


def iniciar_sesion():
    while True:
        dni = input("Ingrese su DNI (8 números): ").strip()
        if dni.isdigit() and len(dni) == 8 and "00000001" <= dni <= "72000000":
                break
        print("Error: Ingrese un DNI válido.")

    hash_contrasenia = obtener_hash(dni)

    if hash_contrasenia is None:
        print(f"ERROR! El usuario con dni {dni} no existe")
        return
    #Despues de verificar separamos el hash de la tupla
    #para evitar errores
    hash_valido = hash_contrasenia[0]

    contrasenia = input("Ingrese su contraseña: ").strip()

    try:
        ph.verify(hash_valido, contrasenia)
        print("Contraseña correcta!")

        buscar_usuario_biometricamente(dni)

    except Exception:
        print("ERROR! Contraseña incorrecta")
        return

def buscar_usuario_biometricamente(dni):
    vector = reconocimiento_facial()
    if vector is None:
        return

    resultado = obtener_vector(dni, vector)

    if resultado:
        nombre, apellido, distancia = resultado

        print(f"Distancia: {distancia:.4f}")

        if distancia < 0.60: #0.60 de umbral es recomendado en la documentación de face_recognition
            print(f"Sesion inciada! Bienvenido {nombre} {apellido}")
        else:
            print("El rostro no coincide con el usuario registrado")
    else:
        print("ERROR!")

def reconocimiento_facial():
    camara = cv2.VideoCapture(0) # Abre la primera cam que encuentra
    print("Iniciando cámara... Presiona 'q' para salir")

    # Obligar a la ventana a saltar al primer plano
    cv2.namedWindow("Escaneando Rostro", cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty("Escaneando Rostro", cv2.WND_PROP_TOPMOST, 1)

    vector_detectado = None

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

            # 1. Dibujamos el recuadro verde sobre el rostro encontrado
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # 2. Dibujamos un fondo relleno para el texto instructivo
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, "ROSTRO DETECTADO", (left + 6, bottom - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # 3. Guardamos el vector
            vector_detectado = rostro_actual_vector

        # Mostramos el video procesado
        cv2.imshow("Escaneando Rostro", frame)

        # ──> MODIFICACIÓN CLAVE:
        # Si ya guardamos un vector en este frame, forzamos a OpenCV a que dibuje la ventana
        # y pausamos la ejecución 1.5 segundos para que el usuario llegue a verse reflejado en la pantalla.
        if vector_detectado is not None:
            cv2.waitKey(1) # Forzar el refresco visual de la ventana antes de congelar
            time.sleep(1.5) # Pausa dramática de 1.5 segundos (puedes cambiarlo a 2.0 si quieres más tiempo)
            break

        # Si no hay rostro, sigue el flujo normal a ~30 FPS esperando la tecla 'q'
        tecla = cv2.waitKey(30) & 0xFF
        if tecla == ord('q'):
            break

    camara.release()
    cv2.destroyAllWindows()

    return vector_detectado