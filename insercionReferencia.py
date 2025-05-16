import re
import json
import random
import psycopg2
import unicodedata
from faker import Faker

MAX: int = int(10e3)

# Llamamos los json con datos para la selección
with open("./data/categorias.json", "r", encoding="utf-8") as f:
    Categorias = json.load(f)
    
with open("./data/proveedores.json", "r", encoding="utf-8") as f:
    Proveedores = json.load(f)

with open("./data/productos.json", "r", encoding="utf-8") as f:
    Productos = json.load(f)

with open("./data/unidadesMedida.json", "r", encoding="utf-8") as f:
    UnidadesMedida = json.load(f)

# Creamos el objeto fake
fake = Faker()

# Conexión a la BD relacional
conn = psycopg2.connect(
	host="localhost",
	database="inventario_emprendimiento",
	user="usuario_emprendimiento",
	password="1234"
)
cur = conn.cursor()

# Función para pasar a campbell keys
def campbellKeyOfString(text: str) -> str:
	text = unicodedata.normalize('NFD', text)
	text = text.encode('ascii', 'ignore').decode('utf-8')
	text = text.lower()
	text = re.sub(r'[^a-z0-9]', '', text)
	return text

# Inserción de datos sobre la tabla "categorias"
for id, categoria in enumerate(Categorias):
	cur.execute("INSERT INTO categorias (id_categoria, nombre) VALUES (%s, %s)",
               (id+1, categoria)
               )
conn.commit()

# Inserción de datos sobre la tabla de "proveedores"
for id, proveedor in enumerate(Proveedores):
	cur.execute("INSERT INTO proveedores (id_proveedor, nombre, correo, telefono) VALUES (%s, %s, %s, %s)",
               (id+1, proveedor, fake.email(domain=f"{campbellKeyOfString(proveedor)}.com"), fake.phone_number())
               )
conn.commit()

# Inserción de datos sobre la tabla "trabajador"
for id in range (30):
	cur.execute("INSERT INTO trabajador (id_trabajador, nombre, telefono, correo, rol) VALUES (%s, %s, %s, %s, %s)",
               (id+1, fake.name(), fake.phone_number(), fake.email(), random.choice(["vendedor", "conserje", "marketing", "ingeniero", "administrador"]))
               )
conn.commit()

# Inserción de datos sobre la tabla "compras"
for id in range (MAX):
	precio_total = round(random.uniform(1e4, 1e6), 2)
	cur.execute("INSERT INTO compras (id_compra, fecha, precio_total, id_proveedor) VALUES (%s, %s, %s, %s)",
               (id+1, fake.date(), precio_total, random.randint(1, len(Proveedores)))
               )
conn.commit()

# Inserción de datos sobre la tabla "productos"
for id, producto in enumerate(Productos):
	precio_unitario = round(random.uniform(1e2, 1e4), 2)
	stock = random.randint(1000, 10000)
	min_stock = random.randint(10, 100)
	cur.execute("INSERT INTO productos (id_producto, nombre, descripcion, precio_unitario, unidad_medida, stock, min_stock, id_categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
               (id+1, producto, "desc general", precio_unitario, random.choice(UnidadesMedida), stock, min_stock, random.randint(1, len(Categorias)))
               )
conn.commit()

# Inserción de datos sobre la tabla "ventas"
for id in range (MAX):
	precio_total = round(random.uniform(1e4, 1e6), 2)
	cur.execute("INSERT INTO ventas (id_venta, fecha, precio_total, id_vendedor) VALUES (%s, %s, %s, %s)",
               (id+1, fake.date(), precio_total, random.randint(1, 30))
               )
conn.commit()

datosProductosCompras = []
setParesProductoCompra = set()
# Inserción de datos sobre la tabla "productos_compras"
for _ in range (MAX):
	# Obtengo un par id_producto y id_compra válidos
	id_producto = random.randint(1, len(Productos))
	id_compra = random.randint(1, MAX)

	# Si la clave existe, siguiente iteración
	if ((id_producto, id_compra) in setParesProductoCompra):
		continue
	setParesProductoCompra.add((id_producto, id_compra))

	# Obtengo el precio unitario de ESE producto
	cur.execute("SELECT precio_unitario FROM productos WHERE id_producto = %s", (id_producto,))
	precio_unitario = cur.fetchone()

	# Si no se encontró, saltamos a la siguiente iteración del for
	if precio_unitario is None:
		continue
	precio_unitario = precio_unitario[0]

	# Cantidad comprada
	cantidad = random.randint(300, 500)

	datosProductosCompras.append((id_producto, id_compra, precio_unitario, cantidad))
try:
	cur.executemany(
		"INSERT INTO productos_compras (id_producto, id_compra, precio_unitario, cantidad) VALUES (%s, %s, %s, %s)",
		datosProductosCompras
	)
except Exception as e:
	print(f"Error sobre la insercion sobre la BD: productos_compras\n Error -> {e} <--")

conn.commit()

datosProductosVentas = []
setParesProductoVenta = set()
# Insercion de datos sobre la tabla "productos_ventas"
for _ in range(MAX):
	# Obtengo un par id_producto y id_venta válidos
	id_producto = random.randint(1, len(Productos))
	id_venta = random.randint(1, MAX)

	# Si la clave existe, siguiente iteración
	if ((id_producto, id_venta) in setParesProductoVenta):
		continue
	setParesProductoVenta.add((id_producto, id_venta))

	# Obtengo el precio unitario de ESE producto
	cur.execute("SELECT precio_unitario FROM productos WHERE id_producto = %s", (id_producto,))
	precio_unitario = cur.fetchone()

	# Si no se encontro, saltamos a la siguiente iteracion del for
	if precio_unitario is None:
		continue
	precio_unitario = precio_unitario[0]

	# Cantidad comprada
	cantidad = random.randint(1, 200)

	datosProductosVentas.append((id_producto, id_venta, precio_unitario, cantidad))

try:
	cur.executemany(
		"INSERT INTO productos_ventas (id_producto, id_venta, precio_unitario, cantidad) VALUES (%s, %s, %s, %s)",
		datosProductosCompras
	)
except Exception as e:
	print(f"Error en la insercion sobre la BD: productos_ventas\n Error -> {e} <--")
conn.commit()

cur.close()
conn.close()