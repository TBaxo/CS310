#goals:
#    - Identify Data Types and Constructors
#    - Identify funtion names and possibly the line they are on
#    -

import re

class Parser:
    """ Parser for Haskell Frontend Application
    
    Basic Parser constructed for sole purpose of running on the dataset given in the same dirctory
    There is very little customisability which may change, however this should suffice for the time being
    
    """

    def __init__(self, filepath):
        self.file = open(filepath)
        
        
    def start_parse(self):
        self.data_types = []
        self.constructors = []
        self.functions = {}
        self.constructor_flag = False
        self.function_flag = False
        #Patterns for regular expressions
        """
        remember to mention some explicit styling for backend to ensure correct parsing
        """
        self.types = re.compile(r"^data|^type")
        self.construct = re.compile(r"^\t[=|]")
        self.funct = re.compile(r"^.* ::")
        self.function_pattern = re.compile(r"^[^=]*=")
        self.empty = re.compile(r"^[\t\n\r\n]*$")
        #start Parsing
        for line in self.file.readlines():
            if self.constructor_flag:
                self.parse_for_constructor(line)
            elif self.function_flag:
                self.parse_for_function(line)
            else:
                self.parse_for_general(line)
    
        
    def parse_for_general(self, line): #goal is to find functions and data types along with their constructors
            #check for data types first
            result = self.types.match(line)
            if result:
                type_name = ((result.string).strip()).split(" ")[1]
                self.data_types.append(type_name)
                #print("now looking for constructors")
                self.constructor_flag = True
            result = self.funct.match(line)
            if result:
                func_name = ((result.string).strip()).split(" ")[0]
                self.functions[func_name] = []
                #print("now looking for pattern matches")
                self.function_flag = True
                

    def parse_for_constructor(self, line):
            result = self.construct.match(line)
            if result:
                self.constructors.append(((result.string).strip()).split(" ")[1])
            elif self.empty.match(line):
                #print("stopped looking for constructors")
                self.constructor_flag = False
    
    def parse_for_function(self, line):
        result = self.function_pattern.match(line)
        if result:
            pattern = result.group().split("=")[0]
            function_name = pattern.split(" ")[0]
            parameters = pattern[len(function_name):].strip()
            self.functions[function_name].append(parameters)
        elif self.empty.match(line):
            self.function_flag = False
    
if __name__ == "__main__":
    p = Parser("data/ass15-2.hs")
    p.start_parse()
    """
    print(str(p.data_types))
    print("\n")
    print(str(p.constructors))
    print("\n")
    print(str(p.functions))
    """
#Start of program
#Important variables
