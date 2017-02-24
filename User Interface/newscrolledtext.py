from tkinter import *
from tkinter import ttk

class ScrolledText(Text):
    
    def __init__(self, master=None):
        Text.__init__(self, master)
        self.yscroll = ttk.Scrollbar(master, orient=VERTICAL, command=self.yview)
        self["yscrollcommand"] = self.yscroll.set
        self.linesframe = ttk.Frame(master, border=0, relief="flat", width=6)
        self["wrap"] = "none"
        self["relief"] = "flat"
        
        self.linenumbers = Text(self.linesframe, width=6, bg="#dde2d9", border=0)
        self.linenumbers["wrap"] = "none"
        self.linenumbers.insert(1.0, "\n")
        self.linenumbers.insert(2.0, "\n")
        self.linenumbers["state"] = "disabled"
        self.linenumbers.tag_configure("linenum", justify="center", relief="flat")
        self.linenumbers.tag_add("linenum", "1.0", "end")
        
        #Grid all the elements
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        
        
        self.grid(column=1, row=0, sticky=(N,E,S,W))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        
        self.linesframe.grid(column=0, row=0, sticky=(N,W,S))
        self.linesframe.rowconfigure(0, weight=1)
        self.linesframe.columnconfigure(0, weight=0)
        
        self.linenumbers.grid(column=0, row=0, sticky=(N,W,S))
        self.linenumbers.rowconfigure(0, weight=1)
        self.linenumbers.columnconfigure(0, weight=0)
        
        self.yscroll.grid(column=2, row=0, sticky=(N,S,W))

if __name__ == "__main__":
    root = Tk()
    textarea = ScrolledText(root)
    root.mainloop()