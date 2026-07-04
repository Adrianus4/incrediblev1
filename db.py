import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://adrian:YMAE0aLvaWg88vrnkjgKyQ@local-canary-17622.jxf.gcp-us-central1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")

# =========================
# CONEXIÓN
# =========================
def get_conn():
    return psycopg2.connect(DATABASE_URL)

# =========================
# CREAR TABLA
# =========================
def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS reclamos (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                nombre STRING,
                tipo STRING,
                descripcion STRING,
                prioridad STRING,
                fecha TIMESTAMP DEFAULT now()
            );
            """)
        conn.commit()

# =========================
# INSERTAR RECLAMO
# =========================
def create_reclamo(nombre, tipo, descripcion, prioridad):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO reclamos (nombre, tipo, descripcion, prioridad)
                VALUES (%s, %s, %s, %s)
            """, (nombre, tipo, descripcion, prioridad))
        conn.commit()

# =========================
# OBTENER RECLAMOS
# =========================
def get_reclamos():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM reclamos ORDER BY fecha DESC")
            return cur.fetchall()
