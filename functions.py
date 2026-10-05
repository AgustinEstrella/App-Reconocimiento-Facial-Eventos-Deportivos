from database import *

def ingreso_usuario():
    #Ingreso DNI
    while True:

        dni = input("Ingrese su DNI (8 números) : ")
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
            nombre = input("Ingrese su nombre, max 15 caracteres").strip()

            #Verificamos longitud y juntamos nombres compuestos
            if 1 >= len(nombre) <= 15 and nombre.replace(" ", "").isalpha():
                nombre = nombre.title() #Formatea primera letra a mayus
                break

            print("Error: Intente nuevamente")

    #Ingreso apellido
    while True:
        apellido = input("Ingrese su apellido, max 15 caracteres").strip()

        #Verificamos longitud y juntamos nombres compuestos
        if 1 >= len(apellido) <= 15 and apellido.replace(" ", "").isalpha():
            apellido = apellido.title() #Formatea primera letra a mayus
            break

        print("Error: Intente nuevamente")

    return dni, nombre, apellido

