import logging
from logging.handlers import RotatingFileHandler

def setupLogger():
    # se crea el logger
    logger = logging.getLogger("logsETL")
    logger.setLevel(logging.DEBUG) # permitimos guardar cualquier tipo de evento

    # crear un RotatingFileHandler, para gestionar el tamaño de los archivos log
    fileHandler = RotatingFileHandler('logs/appETL.log', maxBytes=1000000, backupCount=3)
    fileHandler.setLevel(logging.DEBUG) # permitimos guardar cualquier tipo de evento

    # formato para los logs
    formatter = logging.Formatter('%(asctime)s -> %(levelname)s -> %(message)s')
    fileHandler.setFormatter(formatter)

    # se añade el handler al logger
    logger.addHandler(fileHandler)

    return logger