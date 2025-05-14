# Proyecto guiado – Sistema de Gestión de Inventario para emprendimientos locales

## Requerimientos (Instalar)

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