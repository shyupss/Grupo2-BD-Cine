# Proyecto guiado – Sistema de Gestión de Inventario para emprendimientos locales

## Requerimientos de Base de Datos Cine

### ¿Para qué queremos usar esta base de datos?

Este sistema está diseñado para gestionar de forma eficiente las proyecciones de películas en salas de cine, la venta de tickets, la asignación de asientos por boleto y la trazabilidad del comportamiento del cliente. La información recopilada permitirá realizar análisis comerciales y estratégicos que fortalezcan la toma de decisiones.

---

### Descripción

El sistema gestiona:

- Funciones programadas en distintas salas y horarios.
- Venta de entradas y asignación específica de asientos.
- Registro de clientes y preferencias.
- Datos asociados a películas: género, clasificación, duración, etc.

---

### Objetivo

El objetivo principal es proporcionar una base sólida para la toma de decisiones comerciales a partir del <u>**análisis de los datos**</u>, facilitando acciones como:

- Ajuste de horarios y cartelera según demanda.
- Promociones personalizadas.

---

### Utilidades y Consultas clave

El sistema permitirá responder preguntas relevantes para el negocio, tales como:

- Tendencias de asistencia por día de la semana y horario (por ejemplo, identificar franjas horarias con mayor o menor venta de entradas).
- Recaudación total y segmentada por tipo de sala (2D, 3D, IMAX) y tipo de asiento (reclinable, estándar, VIP).
- Popularidad de películas según su género, duración y clasificación etaria.
- Análisis de comportamiento del público: segmentación por edad, frecuencia de asistencia y preferencias de género cinematográfico.

## Requerimientos/Necesidades del sistema (Instalar)

Para instalar los requerimientos del proyecto, necesitas crear un entorno virtual luego de clonar el repositorio, esto se hace con los siguientes comandos (ejecutar en directorio raíz del proyecto):

```
python -m venv .venv                # Con esto generas el entorno virtual
.\.venv\Scripts\Activate.ps1        # Con esto lo activas
pip install -r requirements.txt     # Con esto instalas las dependencias necesarias para trabajar con el entorno virtual
```

### Notarás que el entorno virtual está activado cuando en tu terminal ves algo del estilo:

```
(.venv) PS C:\...
```

### Importante:
Si quieres instalar más dependencias para hacer pruebas, debes activar nuevamente el entorno virtual en caso de que no esté activado, NO ES NECESARIO TENER EL ENTORNO ACTIVADO PARA TRABAJAR DE FORMA CORRIENTE, solo se activa para instalar dependencias dentro del proyecto, para activar este se utiliza el comando mencionado anteriormente.

Notar que luego de hacer este proceso, en VSCode deberías seleccionar como interprete a Python pero con el entorno virtual como zona de trabajo, esto lo puedes hacer haciendo:

```
"Ctrl + Shift + P" -> Python: Select Interpreter -> Python X.XX ('.venv':venv)
```

Con esto, el entorno virtual debería estar cargado y funcionando correctamente dentro de tu pc localmente.

Por supuesto, aquí tienes la explicación completa en formato markdown, sin emojis, lista para que la copies y pegues en tu README:

---

## Instrucciones de Uso del Sistema Transaccional

**Requisito**: utilizar un entorno virtual venv con las librerías en `requirements.txt` (como se indicó previamente). <br>
El script `modelo-transaccional/crear_db.py` crea una nueva base de datos `cine_db_transaccional` en la conexión del usuario `postgres`.
Allí se alojan las tablas del sistema transaccional y, por lo tanto, también los datos de las transacciones manejadas desde `modelo-transaccional/menu_transacciones.py`.


En el caso de que aún no se haya inicializado la base de datos `cine_db_transaccional`, es necesario ejecutar el script `modelo-transaccional/crear_db.py`:

````markdown
```bash
cd modelo-transaccional/
python crear_db.py
````

Una vez inicializada la base de datos, ya se puede ejecutar `modelo-transaccional/menu_transacciones.py`.

````markdown
```bash
cd modelo-transaccional/
python menu_transacciones.py
````


---

## Instrucciones de Uso del Sistema ETL

**Requisito**: utilizar un entorno virtual venv con las librerías en `requirements.txt` (como se indicó previamente). <br>
El script `modelo-analisis/crear_db.py` crea una nueva base de datos `cine_db_analisis` en la conexión del usuario `postgres`.
Allí se alojan las tablas del sistema de **análisis** o modelo estrella. El sistema ETL leerá los datos en `cine_db_transaccional` y los insertará en `cine_db_analisis`, según las tablas que correspondan.


En el caso de que aún no se haya construido la base de datos `cine_db_analisis`, es necesario ejecutar el script `modelo-analisis/crear_db.py`:

````markdown
```bash
cd modelo-analisis/
python crear_db.py
````

Una vez inicializada la base de datos, ya se puede ejecutar `modelo-analisis/etl.py`.

````markdown
```bash
cd modelo-analisis/
python etl.py
````


---


## Instrucciones de Uso del Análisis de Datos (`analisis.py`)

Este script permite realizar distintos análisis sobre los datos almacenados en la base de datos `cine_db_analisis`.
Al ejecutarlo, se generan gráficos y se muestran datos actualizados automáticamente según la información disponible.
Es fundamental ejecutar el script desde el directorio raíz del proyecto, donde se encuentra el archivo `analisis.py`.

---

### Uso básico
````markdown
```bash
python analisis.py [AÑO]
````

* `[AÑO]`: Corresponde al año para el cual se desea cargar o analizar los datos de ventas (por ejemplo, `2023` o `2024`).
*Importante*: Para efectos de testeo de nuestra base de datos, solo se llenó con datos de enero del 2022 hasta junio de 2025. Si se manejan únicamente los datos suministrados por la plantilla de inserciones de este repositorio, entonces probar solo con esos años.

Ejemplo de uso:

```bash
python analisis.py 2024
```

---

### Descripción del flujo de los scripts

1. Construir `cine_db_transaccional` en usuario `postgres` con `modelo-transaccional/crear_db.py`.
2. Una vez construida `cine_db_transaccional`, ya es posible manipular desde `modelo-transaccional/menu_transaccional.py`.
3. Construir `cine_db_analisis` en usuario `postgres` con `modelo-analisis/crear_db.py`.
4. Ejecutar `modelo-analisis/etl.py`, proceso con scheduler (cada 5 min.). Este sistema ETL primero limpia toda la `cine_db_analisis`. Después lee los datos en `cine_db_transaccional` para volver a llenar `cine_db_analisis`.
5. Ahora, desde el directorio principal, ejecutar `analisis.py` como está indicado en instrucciones. Desde allí, se mostrará un menú para generar los gráficos de análisis.
6. Según la opción escogida en `analisis.py`, se guardan los gráficos en directorio `graficos/`, o bien, actualiza los ya existentes si ya fueron generados para el mismo año.

---

### Consideraciones importantes

* Si no existen datos de ventas para el año solicitado en `analisis.py`, el programa notificará al usuario y no generará gráficos.
* Es necesario que el servidor de PostgreSQL esté activo y configurado correctamente para permitir conexiones.
* El usuario por defecto para la conexión a la base de datos es `postgres` con contraseña `1234`.
* El script `analisis.py` debe ejecutarse siempre desde el directorio raíz del proyecto, para que funcione correctamente.
* Los scripts `modelo-transaccional/crear_db.py`, `modelo-transaccional/menu_transaccional.py`, `modelo-analisis/crear_db.py` y `modelo-analisis/etl.py` deben ejecutarse **siempre** desde sus respectivos directorios.

---

# Drive de nuestro proyecto: 
https://drive.google.com/drive/folders/1VvjUhupeYfJFzTOzafxb42xrqYD864il
