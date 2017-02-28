from tkinter import *
import sys
sys.path.append(r"C:\Users\Thoma\Documents\GitHub\CS310")
sys.path.append(r"C:\Users\Thoma\Documents\GitHub\CS310\Interface")
from Interface.UI import Interface
#from Compiler.compiler import *
from Parser.parser import Parser
from threading import Thread, Lock, Condition, Event
from queue import Queue, Empty


def start_ui():
    interface_thread = Thread(target=run_interface, )
    interface_thread.start()
            

def parse_file(filename):
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
            
def run_interface():
    root = Tk()
    interface = Interface(close_flag, request_queue, response_queue, master=root)
    root.protocol("WM_DELETE_WINDOW", interface.exit_call)
    root.mainloop()
    
def commandloop():
    command = ""
    while(not close_flag.is_set()):
        print("waiting for response")
        try:
            command = request_queue.get(True, 2)
        except Empty:
            continue
        if command[0] == "PARSE":
            print("here")
            result = parse_file(command[1])
            if result != None:
                response_queue.put((result))
            else:
                response_queue.put((None))
        elif command[1] == "CONFIG":
            pass
        else:
            print("invalid command")
            
if __name__ == "__main__":
    request_queue = Queue()
    response_queue = Queue()
    close_flag = Event()
    start_ui()
    commandloop()