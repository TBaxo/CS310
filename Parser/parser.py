#goals:
#    - Identify Data Types and Constructors
#    - Identify funtion names and possibly the line they are on
#    -

import re


#This fuction is used to minimise the input and get rid of all the comments before hand, this may not be useful in the grand scheme of things, however it just gives some utility
#and provides a proof of skill

class Parser:
    """ Parser for Haskell Frontend Application
    
    Basic Parser constructed for sole purpose of running on the dataset given in the same dirctory
    There is very little customisability which may change, however this should suffice for the time being
    
    """

    def __init__(self, filepath):
        self.file = open(filepath)
        
        
    def start_parse(self):
        self.data_types = []
        self.data_type_counter = 0
        self.constructors = []
        self.constructor_counter = 0
        self.functions = []
        self.function_counter = 0
        self.constructor_flag = False
        #Patterns for regular expressions
        self.types = re.compile("^data")
        self.construct = re.compile("^\t[=|]")
        self.funct = re.compile("^.* ::")
        #start Parsing
        for line in self.file.readlines():
            if(self.constructor_flag):
                self.constructor_flag = self.parse_for_constructor(line)
            else:
                self.constructor_flag = self.parse_for_general(line)
    
        
    def parse_for_general(self, line): #goal is to find functions and data types along with their constructors
            #check for data types first
            result = self.types.match(line)
            if result:
                self.data_types.append(((result.string).strip()).split(" ")[1])
                return True
            result = self.funct.match(line)
            if result:
                self.functions.append(((result.string).strip()).split(" ")[0])
                return 

    def parse_for_constructor(self, line):
            result = self.construct.match(line)
            if result:
                self.constructors.append(((result.string).strip()).split(" ")[1])
                return True
            elif(line in ["\r\n", "\n"]):
                return False
    
if __name__ == "__main__":
    p = Parser("data/ass15-2.hs")
    p.start_parse()
    print(str(p.data_types))
    print(str(p.constructors))
    print(str(p.functions))
#Start of program
#Important variables
