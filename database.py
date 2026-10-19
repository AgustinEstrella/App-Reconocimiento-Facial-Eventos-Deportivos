import psycopg2
from pgvector.psycopg2 import register_vector
from config import DB_CONFIG

# Aqui nos conectamos a la db
def establecer_conexion_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG) # Con ** pasamos directamente el diccionario
        register_vector(conn)
        return conn

    except psycopg2.OperationalError as e:
        print(f"ERROR_ No se pudo conectar a la base de datos: {e}")
        raise e

def verificacion_usuario_existente(DNI):
    conn = establecer_conexion_db()
    cursor = conn.cursor()

    #Vemos si el usuario ya se encuentra registrado
    cursor.execute("SELECT dni "
                   "FROM ESPECTADOR "
                   "WHERE dni = %s", (DNI,))

    existe = cursor.fetchone() is not None
    cursor.close()
    conn.close()

    return existe

def creacion_usuario(dni, nombre, apellido):
    conn = establecer_conexion_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO ESPECTADOR (dni, nombre, apellido) "
                       "VALUES (%s, %s, %s);", (dni, nombre, apellido))
        conn.commit()
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def adicion_rostro(vector, dni):
    conn = establecer_conexion_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE ESPECTADOR "
                       "SET biometria = %s "
                       "WHERE dni = %s", (vector, dni))

        conn.commit()
    except Exception as e:
        print(f"Error al adicionar rostro: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def buscar_usuario(vector):
    conn = establecer_conexion_db()
    cursor = conn.cursor()
    try:
        # Antes usabamos distancia coseno (<=>) con deepface
        # ahora con face_recognition usamos distancia euclidea (<->)
        cursor.execute("SELECT dni, nombre, apellido, biometria <-> %s::vector AS distancia "
                       "FROM ESPECTADOR "
                       "WHERE BIOMETRIA IS NOT NULL "
                       "ORDER BY biometria <-> %s::vector "
                       "LIMIT 1;" , (vector, vector))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar usuario: {e}")
    finally:
        cursor.close()
        conn.close()