from tkinter import *
from tkinter import ttk
from configdialog import ConfigDialog
from newscrolledtext import ScrolledText
from tkinter import filedialog
from threading import Thread, Lock, Condition, Event
from queue import Queue, Empty
import sys
sys.path.append(r"C:\Users\Thoma\Documents\GitHub\CS310")
#from Compiler.compiler import *
from Parser.parser import Parser

class Application:


    def __init__(self):
        pass
        
    def start(self):
        
        self.request_queue = Queue()
        self.response_queue = Queue()
        close_flag = Event()
        self.interface_thread = Thread(target=self.run_interface, args=(close_flag,))
        self.interface_thread.start()
        command = ""
        while(not close_flag.is_set()):
            """
            This loop may not be intuitive as is_set() returns false if it is not set
            """
            print("waiting for response")
            try:
                command = self.request_queue.get(True, 2)
            except Empty:
                continue
            if command[0] == "PARSE":
                print("here")
                result = self.parse_file(command[1])
                if result != None:
                    self.response_queue.put((result))
                else:
                    self.response_queue.put((None))
                
    
    def parse_file(self, filename):
        print("parse")
        if filename == None:
                return None
        else:
            if not filename.endswith(".hs"):
                return None
            else:
                p = Parser(filename)
                p.start_parse()
                return (p.data_types, p.constructors, p.functions)
                
    def run_interface(self, close_flag):
        root = Tk()
        self.interface = self.Interface(close_flag, self.request_queue, self.response_queue, master=root)
        root.protocol( "WM_DELETE_WINDOW", self.interface.exit_call)
        root.mainloop()
                
                
                
    class Interface(ttk.Frame):
    
        def __init__(self, close_flag, request_queue, response_queue, master=None):
            self.request_queue, self.response_queue = request_queue, response_queue
            Frame.__init__(self, master)
            self.isClosed = close_flag
            self.master.title("Haskell Frontend Developer")
            self.master = master
            self.master.columnconfigure(0, weight=1)
            self.master.rowconfigure(0, weight=1)
            self.init_window()
            
        def init_window(self):
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.grid(column=0, row=0, sticky=(N,W,E,S))
            
            self.master.option_add('*tearOff', FALSE)
            menu = Menu(self.master)
            self.master["menu"] = menu
            file = Menu(menu)
            file.add_command(label="Parse New File", command=self.parse_result)
            file.add_command(label="Compile", command=self.compile)
            file.add_command(label="Exit", command=self.exit_call)
            menu.add_cascade(label="File", menu=file)
            
            options = Menu(menu)
            options.add_command(label="Config", command=self.config)
            menu.add_cascade(label="Options", menu=options)
            
            self.textframe = ttk.Frame(self)
            self.textframe.grid(column=0, row=0, sticky=(N, E, S, W))
            self.textarea = ScrolledText(self.textframe)
            
            self.textarea.focus()
            
            ttk.Style().configure("B.TFrame", bg="red")
            self.bottomframe = ttk.Frame(self, relief="sunken", style="B.TFrame")
            self.bottomframe.grid(column=0, row=1, sticky=(S, E, W))
            self.bottomframe.columnconfigure(0, weight=2)
            self.bottomframe.rowconfigure(0, weight=2)
            
            #self.StringVars()
            #self.linenumbers = Label()
            
        def compile(self):
            print(self.textarea.get("1.0"))
        
        def get_filepath(self):
            filename = filedialog.askopenfilename()
            return filename
        
        def parse_result(self):
            for var in self.bottomframe.winfo_children():
                var.destroy()
            self.request_queue.put(("PARSE", self.get_filepath()))
            print("bighere")
            response = self.response_queue.get(True)
            if response != None:
                self.text = ttk.Label(self.bottomframe, text="Data Types: {s[0]}\nConstuctors: {s[1]}\nFunctions: {s[2]}".format(s=response), relief="sunken")
                #self.bottomframe.constructors = ttk.Label(self.bottomframe, text= + str(p.constructors))
                #self.bottomframe.functions = ttk.Label(self.bottomframe, text= + str(p.functions))
                #self.bottomframe.data_types.grid()
                #self.bottomframe.constructors.grid()
                #self.bottomframe.functions.grid()
                #self.bottomframe.text["padding"] = (0, 0)
                self.text.grid(column=0, row=0, sticky=(S, W, E))
                self.text.columnconfigure(0, weight=1)
                self.text.rowconfigure(0, weight=1)
            else:
                self.error = ttk.Label(self.bottomframe, text="Invalid File Type", relief="sunken")
                self.error.grid(column=0, row=0, sticky=(S, W, E))
                self.error.columnconfigure(0, weight=1)
                self.error.rowconfigure(0, weight=1)
                print("Invalid File Type")
                
        def config(self):
            dialog = ConfigDialog()
                
        def exit_call(self):
            self.isClosed.set()
            exit()
            
            
            
if __name__ == "__main__":
    app = Application()
    app.start()