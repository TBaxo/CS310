#Compiler code, should compile standard frontend syntax using the haskell backend into a valid haskell String
#simplfy things,only make the fuctions that are available
#consider things like x + 3 + 2 + 4 --potential solutions include counting operators, foldL
format = "Operation Add"
format2 = "Declare (x, y)"
result = "start ["
operator_keywords = {"+": "Operation Add", "-": "Operation Minus", "*": "Operation Multiply", "/": "Operation Divide"}
variables = ("String", "Integer", "Variable") #If these are found that means that this is something the user must input 



input_var = input("enter a front end syntax: \n")
#number of operators need to be counted 
num_operators = input_var.count("+") + input_var.count("-") + input_var.count("*") + input_var.count("/")
print ("Number of Operators is: %d \n-------------" % (num_operators))
add_flag = False
previous_char = ""
result = ""
for chars in input_var.split(" "):
	print(chars)
	if(add_flag == True):
		if(chars.isalpha()):
			result += (" (Symbol \"" + chars + "\")")
		else:
			result += (" (Value " + chars + ")")
		add_flag = False
		continue
	if(chars in operator_keywords.keys()):
		result += (operator_keywords[chars] + previous_char)
		add_flag = True
		continue
	if(chars.isalpha()):
		previous_char = (" (Symbol \"" + chars + "\")")
	else:
		previous_char = (" (Value " + chars + ")")
print(result)
#now parse front end with gve number of operators, assume infix, return in haskell format
