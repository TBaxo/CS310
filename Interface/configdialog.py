from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askstring

import re

class ConfigDialog(Toplevel):
    
    def __init__(self, master=None, parse_data=None):
        Toplevel.__init__(self, master)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)
        self.title("Configure Settings")
        self.initialise_window(parse_data)
        
    def initialise_window(self, parse_data):
        self.functions = parse_data[2]
        self.values = {}
        self.bindings = {}
        for var in self.functions:
            self.values[var] = {}
            print(self.functions[var])
            for var2 in self.functions[var]:
                self.values[var][var2] = [None]
                
        self.start_param = {}
        
        self.left_window = ttk.Frame(self)
        self.right_window = ttk.Frame(self)
        self.left_label_frame = ttk.Labelframe(self.left_window, text="Functions")
        self.separator = ttk.Separator(self, orient="vertical")
        self.right_label = ""
        self.right_label_frame = ttk.Labelframe(self.right_window)
        
        #listbox setup
        self.function_names = list(self.functions.keys())
        self.listbox_entries = ["General"]
        self.listbox_entries.extend(self.function_names)
        print(self.listbox_entries)
        listbox_entries_var = StringVar(value=self.listbox_entries)
        self.left_listbox = Listbox(self.left_label_frame, listvariable=listbox_entries_var)
        self.left_listbox.select_set(0)
        
        #bind events
        self.left_listbox.bind("<<ListboxSelect>>", self.show_function_options)
        self.left_listbox.event_generate("<<ListboxSelect>>")
        
        #grid the elements
        self.left_window.grid(column=0, row=0, sticky=(N,E,S,W))
        self.right_window.grid(column=2, row=0, sticky=(N,E,S,W))
        self.left_label_frame.grid(column=0, row=0, sticky=(N,E,S,W), padx=10, pady=10)
        self.left_listbox.grid(column=0, row=0, sticky=(N,E,S,W), padx=20, pady=20)
        self.separator.grid(column=1, row=0, sticky=(N,E,S,W))
        self.right_label_frame.grid(column=0, row=0, sticky=(N,E,S,W), padx=10, pady=10)
        
        #grid configure
        self.left_window.columnconfigure(0, weight=1)
        self.left_window.rowconfigure(0, weight=1)
        
        self.left_label_frame.columnconfigure(0, weight=1)
        self.left_label_frame.rowconfigure(0, weight=1)
        
        self.left_listbox.columnconfigure(0, weight=1)
        self.left_listbox.rowconfigure(0, weight=1)
        
        self.right_window.columnconfigure(2, weight=1)
        self.right_window.rowconfigure(0, weight=1)
        
        self.right_label_frame.columnconfigure(0, weight=1)
        self.right_label_frame.rowconfigure(1, weight=1)
        
    def show_function_options(self, *args):
        indexs = self.left_listbox.curselection()
        index = indexs[0]
        print(index)
        name = self.listbox_entries[index]
        if name in list(self.start_param.keys()):
            return None
        self.right_label = name
        self.right_label_frame["text"] = name
        if name == "General":
            self.show_general()
        else:
            self.construct_tree(self.listbox_entries[index])
        
        #self.right_label
        
    def show_general(self):
        """
        
        geeral options include, starting function, and the parameter for which to pass all your statements as. 
        
        """
        for var in self.right_label_frame.winfo_children():
            var.destroy()
            
        self.comboselection = StringVar()
        self.combobox = ttk.Combobox(self.right_label_frame, textvariable=self.comboselection)
        self.combobox["values"] = tuple(self.function_names)
        
        def select_start_output(*args):
            selection = self.comboselection.get()
            output = askstring("Config Dialog","Enter desired output bind:")
            self.start_param[selection] = output
            
        self.combobox.bind('<<ComboboxSelected>>', select_start_output)
        
        label = ttk.Label(self.right_label_frame, text="Start Function")
        
        label.grid(column=0, row=0, sticky=(N))
        self.combobox.grid(column=0, row=1, sticky=(N), padx=40)
        self.combobox.rowconfigure(1, weight=0)
        label.rowconfigure(0, weight=0)
        
    
    def construct_tree(self, name):
        #treeview setup
        for var in self.right_label_frame.winfo_children():
            var.destroy()
        self.right_treeview = ttk.Treeview(self.right_label_frame, columns=("pattern","symbol","output"))
        self.right_treeview.bind("<<TreeviewSelect>>", self.add_binding) 
        self.right_treeview["show"] = "headings"
        #self.right_treeview.column("pattern", anchor="w")
        #self.right_treeview.column("symbol", anchor="w")
        self.right_treeview.heading("symbol", text="Symbol", anchor="w")
        self.right_treeview.heading("pattern", text="Pattern", anchor="w")
        self.right_treeview.heading("output", text="Output", anchor="w")
        for pattern in self.functions[name]:
            symbol = self.values[name][pattern][0]
            if symbol == None:
                self.right_treeview.insert("", "end", values=((pattern,)))
            else:
                output = self.values[name][pattern][1]
                self.right_treeview.insert("", "end", values=((pattern, symbol, output)))
        self.right_treeview.grid(column=0, row=0, sticky=(N,E,S,W), padx=20, pady=20)
        
    def add_binding(self, *args):
        index = self.right_treeview.focus()
        item = self.right_treeview.item(index)["values"][0]
        print(item)
        symbol = askstring("Config Dialog","Enter Symbol to bind:")
        if symbol == None:
            pass
        else:
            output = askstring("Config Dialog","Enter desired output bind:")
            if output == None:
                return None
            indexs = self.left_listbox.curselection()
            index = indexs[0]
            name = self.listbox_entries[index]
            self.values[name][item] = [symbol, output]
            self.bindings[symbol] = output
            self.construct_tree(name)
        