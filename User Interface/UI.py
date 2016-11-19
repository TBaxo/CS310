from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sys
sys.path.append(r"C:\Users\Thoma\Documents\GitHub\CS310")
from Compiler.compiler import *
from Parser.parser import Parser
print(dir())
class Application (Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.prev_parse = False
        self.master = master
        self.init_window()
        
    def init_window(self):
        self.master.title("Haskell Frontend Developer")
        self.pack(fill=BOTH, expand=1)
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Parse New File", command=self.parse_file)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        self.textarea = ScrolledText(self)
        self.textarea.pack(fill=BOTH, expand=1)
        self.bottomframe = Frame(self, bd=3, relief="sunken")
        self.bottomframe.pack(side=BOTTOM, fill=X)
        
    def parse_file(self):
        from tkinter import filedialog
        dialog = filedialog.LoadFileDialog(self.master)
        dialog.top.geometry("900x500")
        filename = dialog.go()
        if filename == None:
            return None
        else:
            p = Parser(filename)
            p.start_parse()
            if self.prev_parse:
                self.bottomframe.data_types.destroy()
                self.bottomframe.constructors.destroy()
                self.bottomframe.functions.destroy()
            self.bottomframe.data_types = Label(self.bottomframe, text="Data Types: " + str(p.data_types))
            self.bottomframe.constructors = Label(self.bottomframe, text="Constuctors: " + str(p.constructors))
            self.bottomframe.functions = Label(self.bottomframe, text="Functions: " + str(p.functions))
            self.bottomframe.data_types.pack()
            self.bottomframe.constructors.pack()
            self.bottomframe.functions.pack()
            self.prev_parse = True
    
    def client_exit(self):
        exit()
        
root =  Tk()
root.geometry("400x300")
app = Application(root)
root.mainloop()