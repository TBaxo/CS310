#goals:
#	- Identify Data Types and Constructors
#	- Identify funtion names and possibly the line they are on
#	-

import re


#This fuction is used to minimise the input and get rid of all the comments before hand, this may not be useful in the grand scheme of things, however it just gives some utility
#and provides a proof of skill

def minimise():
	comment_flag = False
	newline_flag = False
	for line in f.readlines():
		if(comment_flag):
			if("--}" in line):
				comment_flag = False
				newline_flag = False
			continue
		else:
			if("{--" in line):
				comment_flag = True
				continue
			if(line in ["\n" , "\r\n"] and newline_flag == False):
				print(line.strip())
				newline_flag = True
			elif(line not in ["\n" , "\r\n"] and newline_flag == True):
				newline_flag = False
			if(newline_flag == True):
				continue
		print(line.strip())		
	return
	
def parse_for_general(): #goal is to find functions and data types along with their constructors
		#check for data types first
		result = types.match(line)
		if result:
			data_types.append(((result.string).strip()).split(" ")[1])
			return True
		result = funct.match(line)
		if result:
			functions.append(((result.string).strip()).split(" ")[0])
			return 

def parse_for_constructor():
		print("looking for constructors")
		result = construct.match(line)
		if result:
			constructors.append(((result.string).strip()).split(" ")[1])
		elif(line in ["\r\n", "\n"]):
			return False

	
	
#Start of program
#Important variables
f = open("data/ass15-2.hs")
data_types = []
data_type_counter = 0
constructors = []
constructor_counter = 0
functions = []
function_counter = 0
constructor_flag = False

types = re.compile("^data")
construct = re.compile("=.* | \|")
funct = re.compile("^.* ::")
for line in f.readlines():
	if(constructor_flag):
		constructor_flag = parse_for_constructor()
	else:
		constructor_flag = parse_for_general()
	
print("The data types found are: ") 
print(data_types)
print("The Constuctors found are: ")
print(constructors)
print("The functions found are: ")
print(functions)

#minimise()
