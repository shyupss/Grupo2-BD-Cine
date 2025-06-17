from . import tk, Callable

class Entry(tk.Entry):
    
    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas, **kwargs):
        self.__texto:tk.StringVar = tk.StringVar()
        super().__init__(master, textvariable=self.__texto, **kwargs)

        self.__limite_caracteres:int = -1
        self.__caracteres_prohibidos:str|list|set|tuple|dict = ""
        
        self.__placeholder:str = ""
        self.__placeholder_color_normal:str = self.cget("foreground")
        self.__placeholder_color:str = "gray"
        self.__usando_placeholder:bool = False

        self.__exe_al_escribir:Callable = None
        self.__exe_focus_out:Callable = None
        self.__exe_focus_in:Callable = None

        self.__texto.trace_add('write', self.__exe_al_escribir_f)
        self.configure(validate='key', validatecommand=(self.register(self.__validar_entrada_f), '%P'),)
        self.bind("<FocusOut>", self.__exe_focus_out_f)
        self.bind("<FocusIn>", self.__exe_focus_in_f)

        self.__exe_focus_out_f()

    @property
    def texto(self):
        if self.__usando_placeholder: return ""
        else: return self.__texto.get()
    
    @texto.setter
    def texto(self, txt:str):
        self.__texto.set(txt)

    @property
    def limite_caracteres(self):
        return self.__limite_caracteres
    
    @limite_caracteres.setter
    def limite_caracteres(self, limite:int):
        self.__limite_caracteres = limite

    @property
    def caracteres_prohibidos(self):
        return self.__caracteres_prohibidos
    
    @caracteres_prohibidos.setter
    def caracteres_prohibidos(self, nueva_coleccion:str|list|set|tuple|dict):
        self.__caracteres_prohibidos = nueva_coleccion

    @property
    def placeholder(self):
        return self.__placeholder
    
    @placeholder.setter
    def placeholder(self, texto:str):
        self.__placeholder = texto

    @property
    def exe_al_escribir(self):
        return self.__exe_al_escribir
    
    @exe_al_escribir.setter
    def exe_al_escribir(self, exe:Callable):
        self.__exe_al_escribir = exe

    @property
    def exe_focus_out(self):
        return self.__exe_focus_out
    
    @exe_focus_out.setter
    def exe_focus_out(self, exe:Callable):
        self.__exe_focus_out = exe

    @property
    def exe_focus_in(self):
        return self.__exe_focus_in
    
    @exe_focus_in.setter
    def exe_focus_in(self, exe:Callable):
        self.__exe_focus_in = exe

    @property
    def usando_placeholder(self):
        return self.__usando_placeholder

    def __exe_al_escribir_f(self, *_):
        if self.__exe_al_escribir: self.__exe_al_escribir()

    def __exe_focus_out_f(self, *_):
        if not self.__texto.get() and self.__placeholder:
            self.__usando_placeholder = True
            self.__texto.set(self.__placeholder)
            self.config(foreground=self.__placeholder_color)

        if self.__exe_focus_out: self.__exe_focus_out()

    def __exe_focus_in_f(self, *_):
        if self.__usando_placeholder and self.__texto.get() == self.__placeholder:
            self.__texto.set("")
            self.__usando_placeholder = False
            self.config(foreground=self.__placeholder_color_normal)

        if self.__exe_focus_in: self.__exe_focus_in()

    def __validar_entrada_f(self, entrada:str):
        if self.__usando_placeholder: return True

        if any(c in entrada for c in self.__caracteres_prohibidos): return False
        if len(entrada) > self.__limite_caracteres > -1: return False

        return True