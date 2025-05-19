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

# Drive de nuestro proyecto: 
https://drive.google.com/drive/folders/1VvjUhupeYfJFzTOzafxb42xrqYD864il
