from . import tk

class Tk(tk.Tk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.bind_all("<Button-1>", self.__focus_on_click, add='+')

    def __focus_on_click(self, event:tk.Event):
        '''Actualiza el focus de la App al Widget que fue clieckeado.'''
        widget:tk.Widget = event.widget
        try: widget.focus_set()
        except: self.focus_set()