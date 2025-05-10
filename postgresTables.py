# importamos librerías
from libraries import *

# Conexión a PostgreSQL
conn = pcg.connect(
	host="localhost",
	database="tutorial_python",
	user="python_user",
	password="1234"
)

cur = conn.cursor()

# Crear una tabla de ejemplo
cur.execute("""
	CREATE TABLE IF NOT EXISTS ejemplo (
    	id SERIAL PRIMARY KEY,
    	nombre VARCHAR(100)
	);
""")
conn.commit()

# Insertar datos
cur.execute("INSERT INTO ejemplo (nombre) VALUES (%s)", ("Juan",))
conn.commit()

# Consultar datos
cur.execute("SELECT * FROM ejemplo;")
filas = cur.fetchall()
for fila in filas:
	print(fila)

# Cerrar conexión
cur.close()
conn.close()