from . import tk, Callable

class Button(tk.Button):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):
        self.__texto:tk.StringVar = tk.StringVar()
        self.__exe_boton:Callable = None

        super().__init__(master, textvariable=self.__texto, command=self.__click_boton, **kwargs)

    @property
    def texto(self):
        return self.__texto.get()
    
    @texto.setter
    def texto(self, txt:str):
        self.__texto.set(txt)

    @property
    def exe_boton(self):
        return self.__exe_boton
    
    @exe_boton.setter
    def exe_boton(self, exe:Callable):
        self.__exe_boton = exe

    def __click_boton(self, *_):
        if self.__exe_boton: self.__exe_boton()