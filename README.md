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

El objetivo principal es proporcionar una base sólida para la toma de decisiones comerciales a partir del análisis de los datos, facilitando acciones como:

- Ajuste de horarios y cartelera según demanda.
- Promociones personalizadas.
- Optimización de la distribución de salas y precios.

---

### Utilidades y Consultas clave

El sistema permitirá responder preguntas relevantes para el negocio, tales como:

- Tendencias de asistencia por día de la semana y horario (por ejemplo, identificar franjas horarias con mayor o menor venta de entradas).
- Recaudación total y segmentada por tipo de sala (2D, 3D, IMAX) y tipo de asiento (reclinable, estándar, VIP).
- Popularidad de películas según su género, duración y clasificación etaria.
- Análisis de comportamiento del público: segmentación por edad, frecuencia de asistencia y preferencias de género cinematográfico.

---

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

## Instrucciones de Uso del Análisis de Datos (`analisis.py`)

Este script permite realizar distintos análisis sobre los datos almacenados en la base de datos `db_cine`.
Al ejecutarlo, se generan gráficos y se muestran datos actualizados automáticamente según la información disponible.
Es fundamental ejecutar el script desde el directorio raíz del proyecto, donde se encuentra el archivo `analisis.py`.

---

### Uso básico
````markdown
```bash
python analisis.py [AÑO]
````

* `[AÑO]`: Corresponde al año para el cual se desea cargar o analizar los datos de ventas (por ejemplo, `2023` o `2020`).

Ejemplo de uso:

```bash
python analisis.py 2023
```

---

### Descripción del flujo del script

1. El script pregunta si se desea crear la base de datos `db_cine` junto con su esquema correspondiente.
2. Solicita la contraseña del usuario `postgres` para realizar las operaciones necesarias.
3. Verifica si la base de datos y los usuarios ya existen y omite su creación si es así.
4. Ofrece la opción de insertar datos de prueba en la base de datos.
5. Se conecta como el usuario `user_cine` a la base de datos `db_cine`.
6. Presenta un menú con las distintas opciones de análisis que el usuario puede elegir para obtener información relevante.

---

### Opciones de análisis disponibles

Al iniciar el script, se muestra un menú con las siguientes opciones:

1. Top 10 de las películas más vistas
2. Top 10 de géneros menos vistos
3. Ventas en un año particular
4. Ventas por género en un año específico
5. Edad promedio del público por género de películas
6. Consulta adicional en desarrollo

Para cada análisis seleccionado, el programa:

* Genera y muestra un gráfico correspondiente.
* Muestra los datos en consola.
* Guarda el gráfico o actualiza el existente si ya fue generado antes.

---

### Consideraciones importantes

* El script reutiliza los datos ya existentes en la base de datos y actualiza los gráficos con información vigente.
* Si no existen datos de ventas para el año solicitado, el programa notificará al usuario y no generará gráficos.
* Es necesario que el servidor de PostgreSQL esté activo y configurado correctamente para permitir conexiones.
* El usuario por defecto para la conexión a la base de datos es `user_cine` con contraseña `1234`, a menos que se haya modificado.
* El script debe ejecutarse siempre desde el directorio raíz del proyecto, para que funcione correctamente.

---

# Drive de nuestro proyecto: 
https://drive.google.com/drive/folders/1VvjUhupeYfJFzTOzafxb42xrqYD864il
