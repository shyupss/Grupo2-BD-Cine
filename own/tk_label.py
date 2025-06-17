from . import tk, Callable

class Label(tk.Label):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas, **kwargs):
        self.__texto:tk.StringVar = tk.StringVar()
        self.__exe_al_escribir:Callable = None
        super().__init__(master, textvariable=self.__texto, **kwargs)

    @property
    def texto(self):
        return self.__texto.get()
    
    @texto.setter
    def texto(self, txt:str):
        if not isinstance(txt, str): raise ValueError("El valor asignado al 'own.Label.texto' debe ser una cadena de texto 'str'.")
        if self.__exe_al_escribir: self.__exe_al_escribir()
        self.__texto.set(txt)

    @property
    def exe_escritura(self):
        return self.__exe_al_escribir
    
    @exe_escritura.setter
    def exe_escritura(self, exe:Callable):
        if not isinstance(exe, Callable): raise ValueError("El valor asignado al 'own.Label.exe_escritura' debe ser una función 'Callable'.")
        self.__exe_al_escribir = exe