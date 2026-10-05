import psycopg2
from pgvector.psycopg2 import register_vector
from config import DB_CONFIG

def establecer_conexion_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG) # Con ** pasamos directamente el diccionario
        register_vector(conn)
        return conn

    except psycopg2.OperationalError as e:
        print(f"ERROR_ No se pudo conectar a la base de datos: {e}")
        raise e

def verificacion_usuario_existente(DNI):
    #Vemos si el usuario ya se encuentra registrado
    conn = establecer_conexion_db()
    cursor = conn.cursor()

    cursor.execute("SELECT dni"
                   "FROM ESPECTADOR"
                   "WHERE dni = %s", (DNI,))

    existe = cursor.fetchone() is not None
    return existe

def adicion_usuario(dni, nombre, apellido):
    conn = establecer_conexion_db()
    cursor = conn.cursor()
