{--

CS256 COURSEWORK -- MYSTREY BACKEND BY THOMAS BAXENDALE

Interface: dec, evaluate, assign, evaluateBool, conditional, whileDo, execute and start

Data Types: Statement, Expression and Operator

Research Sources:
http://www.cs.kent.ac.uk/people/staff/sjt/craft2e/errors/allErrors.html
http://learnyouahaskell.com/making-our-own-types-and-typeclasses
https://www2.warwick.ac.uk/fac/sci/dcs/teaching/material/cs256/2.4.pdf
http://dev.stephendiehl.com/fun/002_parsers.html
http://stackoverflow.com/questions/16970431/implementing-a-language-interpreter-in-haskell
https://wiki.haskell.org/Haskell_programming_tips#Choose_types_properly
https://www.haskell.org/tutorial/goodies.html

--}

{-- Data Types --}
{--
The first data type I created is the Statement data type, this models the statements in Mystrey into a Haskell form and is used for pattern matching to select 
the correct functions for the different statements.
The types of statements are: Declare, Assign, If, Composition and While.

The next data type is the Expression data tpye, this models arithmetic operations, Integer values for variables and Symbols for varibale names.
The Operation instance of Expression takes 3 parameters, an Operator and 2 other Expressions.

The last data type I made is the Operator data type, this models arithmetic and logical operators as seen below, this data type is only used when 
using the Operation instance of the Expression data type to tell functions which operator is to be used.
The operators Add, Minus, Divide, Multiply, Less Than, Greater Than, Equal to, Less than or equal to, Greater than or equal to.
There are also 2 extras which are AND and OR.

The last type I made is the Variable type, this is not a new data type as it is made using 2 existing data types, Variable models what variables would look
like in a permanent store i.e. A string variabe name and an Integer for the value
--}

data Statement
	= Declare Variable 
	| Assign String Expression
	| If Expression [Statement]
	| Composition [Statement]
	| While Expression Statement
	
data Expression 
	= Operation Operator Expression Expression 
	| Value Integer
	| Symbol String

data Operator 
	= Add 
	| Minus 
	| Multiply 
	| Divide
	| Lt
	| Gt
	| Eq
	| LtEq
	| GtEq
	| And
	| Or
	
type Variable = (String, Integer)



start :: [Statement] -> [Variable] -> [Variable]
start [] (x:l) = (x:l)
start (s:sl) [] = start (sl) (execute s [])
start (s:sl) (x:l) = start (sl) (execute s (x:l))