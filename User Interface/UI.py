from tkinter import *
import sys

class Application (Frame):
    text_exists = False
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
    def init_window(self):
        self.master.title("Haskell Frontend Developer")
        self.pack(fill=BOTH, expand=1)
        #code for adding menu bar, will most likely replace button
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        #file.add_command(label)
        file.add_command(label="Parse New File", command=self.parse_file)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        
    def parse_file(self):
        from tkinter import filedialog
        dialog = filedialog.LoadFileDialog(self.master)
        dialog.top.geometry("900x500")
        filename = dialog.go()
        if not filename == None:
            if self.text_exists:
                pass
            else:
                self.text = Label(self, text="File Successfully Parsed!")
                self.text.pack()
                self.text_exists = True
        else:
            self.text.destroy()
    
    def client_exit(self):
        exit()
        
root =  Tk()
root.geometry("400x300")
app = Application(root)
app.mainloop()