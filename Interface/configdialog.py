from tkinter import *
from tkinter import ttk
class ConfigDialog(Toplevel):
    
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title("Configure Settings")
