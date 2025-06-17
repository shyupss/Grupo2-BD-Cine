from . import tk, Callable

class FrameLabel(tk.LabelFrame):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):
        '''tk.LabelFrame - Widget funciona como Frame pero enmarcado y con texto de titulo.'''
        self.__exe_al_escribir:Callable = None
        super().__init__(master, **kwargs)

    @property
    def texto(self):
        return self['text']
    
    @texto.setter
    def texto(self, txt:str):
        if not isinstance(txt, str): raise ValueError("texto debe ser una cadena de texto") # <--- (?)
        if self.__exe_al_escribir: self.__exe_al_escribir()
        self.config(text=txt)

    @property
    def exe_escritura(self):
        return self.__exe_al_escribir
    
    @exe_escritura.setter
    def exe_escritura(self, exe:Callable):
        if not isinstance(exe, Callable): raise ValueError("El valor asignado al 'own.Label.exe_escritura' debe ser una función 'Callable'.")
        self.__exe_al_escribir = exe