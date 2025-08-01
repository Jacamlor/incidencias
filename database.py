import psycopg2
import os
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")

def get_connection():
    return psycopg2.connect(SUPABASE_URL)

def init_db():
    pass  # Las tablas ya están creadas en Supabase

def insertar_albaran(numero, tienda, cantidad):
    fecha = datetime.now()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO albaranes (numero_albaran, tienda, cantidad_enviada, cantidad_actual, fecha_subida)
        VALUES (%s, %s, %s, %s, %s)
    """, (numero, tienda, cantidad, cantidad, fecha))
    conn.commit()
    conn.close()

def obtener_albaranes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT numero_albaran FROM albaranes")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

def ajustar_cantidad_albaran(numero_albaran, ajuste, tipo):
    factor = 1 if tipo == "Sumar" else -1
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE albaranes
        SET cantidad_actual = cantidad_actual + %s
        WHERE numero_albaran = %s
    """, (factor * ajuste, numero_albaran))
    conn.commit()
    conn.close()

def registrar_incidencia(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO incidencias (numero_albaran, tienda, tipo, descripcion, estado,
                                 cantidad_ajustada, tipo_ajuste, usuario, fecha_hora)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    conn.close()

def obtener_incidencias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM incidencias")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()
    return rows, columns
