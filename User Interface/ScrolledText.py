__all__ = ['ScrolledText']

from tkinter import *
from tkinter.constants import RIGHT, LEFT, Y, BOTH
from tkinter import ttk

class ScrolledText(Text):
    def __init__(self, master=None, **kw):
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.grid(row=0, column=1, sticky=(N,E,S))

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, **kw)
        self.grid(row=0, column=0, sticky=(N,E,S,W))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)
        
def example():
    stext = ScrolledText()
    stext.grid(column=0, row=0, sticky=(N, W, E, S))
    stext.columnconfigure(0, weight=1)
    stext.rowconfigure(0, weight=1)
    stext.mainloop()

if __name__ == "__main__":
    example()
    