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


{--
The two functions detailed below are the essential functions I created to allow sample Mystrey Programs be created.

The start function takes 2 parameters, a list of statements and a list of declared variables. At the beginning the list of variables will be empty,
but as the prorgam progresses the list will increase in size.
The way the start function works is that when start is called, it runs start on the tail of the list of statements, and the return variable list from the
execute function which takes as parameters the head of the statement list and current list of variables. This ensures that after one Mystrey statement is 
executed the variables created from the last statement are passed to the next statement to be executed.

The execute function mentioned above is what handles each individual statement, it takes a single statement and the list of
variables that the have been declared as parameters. For any statement given it will check the pattern matching and if there is a matching pattern
then the correct function will be chosen to handle the given statement.

If a Declare statement is given then it will pass the given parameters to the function dec, there are 2 base cases for this function, one where a variable list is atleast one element
and one where it has no currently declared variables

If an Assign Statement is given then it will pass the given parameters in the statement to the assign function

If an If Statement is given then it will pass the given parameters in the statement to the conditional function

If a Composition Statement is given then then one of 2 cases are matched.
One where there are no more statements to be executed in the composition and one where there are still more statements to be executed.
The other is when there are no statements left in the composition then the variable list is returned, when there are statements left in the composition, then it executes the 
tail of the statement list with the variables given from executing the head of the statement list.

If a While Statement is given then it will pass the given parameters in the statement to the whileDo function

--}



start :: [Statement] -> [Variable] -> [Variable]
start [] (x:l) = (x:l)
start (s:sl) [] = start (sl) (execute s [])
start (s:sl) (x:l) = start (sl) (execute s (x:l))


execute :: Statement -> [Variable] -> [Variable]
execute (Declare (x, y)) [] = dec (x, y) []
execute (Declare (x, y)) ((c,n):l) = dec (x, y) ((c,n):l)
execute (Assign (v) (x)) ((c,n):l) = assign (v) (x) ((c,n):l) 
execute (If (x) (s:s':[])) ((c,n):l) = conditional (x) (s:s':[]) ((c,n):l)
execute (Composition ([])) ((c,n):l) = ((c,n):l)
execute (Composition (s:sl)) ((c,n):l) = execute (Composition (sl)) (execute (s) ((c,n):l))
execute (While (x) (s)) ((c,n):l) = whileDo (x) (s) ((c,n):l)


{--
DECLARATION
The function below is a simple model of how variable declaration would work
in an imperative programming language.

The list given to haskell as an input would be the initial list of variables from the permanent store
then all haskell needs to do is take the new variable and value given in the form of a tuple and append it
it either the front or the back of the list. I chose to append it to the front since a variable that has just been
declared is most likely to be used before any other and so it makes sense in terms of efficiency to have it at the front.


--}


dec :: (Variable) -> [Variable] -> [Variable]
dec (c,n) []  = [(c,n)]
dec (c,n) (x:l) =  ((c,n):x:l)

{--
ASSIGNMENT

For variable assignment, I have created a function 'evaluate' which handles data of the expression type, in this case 
only expressions with the operation constructor, this is the function used to take an expression and 
reduce it to a single integer that can be assigned to a variable.

The next step was creating an 'assign' function which took a String representing the variable name, a list of variables and an Expression.
The first job of the function is to recursively check through the list of variables to find the variable we want to change.
This is done by using the inputted Stringand checking for equality with the String part of the stored variables, once the equality
has been found the function will then edit that particular element in the list by exchanging the integer value of the variable with the result of the 
evaluated expression.

--} 




evaluate :: Expression -> [Variable] -> Integer
evaluate (Value x) ((c,n):l) = x
evaluate (Symbol x) ((c,n):l) = if x == c then n
									else evaluate (Symbol x) (l)
evaluate (Operation Add (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) + evaluate (y) ((c,n):l)
evaluate (Operation Minus (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) - evaluate (y) ((c,n):l)
evaluate (Operation Multiply (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) * evaluate (y) ((c,n):l)
evaluate (Operation Divide (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) `div` evaluate (y) ((c,n):l)


assign :: [Char] -> Expression -> [Variable] -> [Variable]
assign (v) (x) [] = error "No value in the list"
assign (v) (x) ((c, n):l) = if v == c then (c, evaluate (x) ((c, n):l)):l
										else (c,n):(assign v x l)

{--
Conditional Statement

I created a new function evaluateBool which takes an expression and the list of variables, and returns 
a boolean. This is essential to evaluating a predicate that is to be given to a conditional statement.

Then I created a function 'conditional' which takes parameters of an expression, a list containing 2 statements and the list of variables.
The function evaluates the boolean expression and checks whether if it is true or false.
If true it runs the first statement in the list, if false it runs the second.

--}

evaluateBool :: Expression -> [Variable] -> Bool
evaluateBool (Operation Lt (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) < evaluate (y) ((c,n):l)
evaluateBool (Operation Gt (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) > evaluate (y) ((c,n):l)
evaluateBool (Operation Eq (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) == evaluate (y) ((c,n):l)
evaluateBool (Operation LtEq (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) <= evaluate (y) ((c,n):l)
evaluateBool (Operation GtEq (x) (y)) ((c,n):l) = evaluate (x) ((c,n):l) >= evaluate (y) ((c,n):l)
evaluateBool (Operation And (x) (y)) ((c,n):l) = if (evaluateBool (x) ((c,n):l) == True) && (evaluateBool (y) ((c,n):l) == True) then True
																												else False
evaluateBool (Operation Or (x) (y)) ((c,n):l) = if (evaluateBool (x) ((c,n):l) == False) && (evaluateBool (y) ((c,n):l) == False) then False
																												else True
																												
conditional :: Expression -> [Statement] -> [Variable] -> [Variable]
conditional (x) (s:s':[]) ((c,n):l)	= if (evaluateBool (x) ((c,n):l) == True) then execute (s) ((c,n):l)
																			else execute (s') ((c,n):l)																			




{--
While..Do..

For my 'While Do' loop I have created a function named whileDo which takes 3 parameters: an Expression, a Statement, and a list fo variables.
The function evaluates the boolean expression it is given using evaluateBool and checks if it is true or false, if it is true then the whileDo
function is recursively called again, except the value of the variable list is now the list that is given after executing the statement that was given
as an argument. This will carry on until evaluateBool returns false at which point the list of variables is returned.
--}

whileDo :: Expression -> Statement -> [Variable] -> [Variable]
whileDo (x) (s) ((c,n):l) = if ((evaluateBool (x) ((c,n):l)) == True) then whileDo (x) (s) (execute (s) ((c,n):l))
																	else ((c,n):l)




{-- Example Programs --}
{--

Int x = 6;
if (x == 0) then { x := 1}
			else { x := 2}
x := x + 4;
		^
		|
start [Declare ("x", 6), If (Operation Eq (Symbol "x") (Value 0)) [Assign "x" (Value 1), Assign "x" (Value 2)], Assign "x" (Operation Add (Symbol "x") (Value 4))] []

Int x = 1;
if (x == 0) then {x := x + 2; 
				  x := x * 10;}
			else {x := 2;}
			^
			|
start [Declare ("x", 0), If (Operation Eq (Symbol "x") (Value 0)) [(Composition [Assign "x" (Operation Add (Symbol "x") (Value 2)), Assign "x" (Operation Multiply (Symbol "x") (Value 10))]), (Composition [Assign "x" (Value 2)])]] []

Int x = 0;
While (x < 5) do {x = x + 1;}
			^
			|
start [Declare ("x", 0), While (Operation Lt (Symbol "x") (Value 5)) (Assign "x" (Operation Add (Symbol "x") (Value 1)))] [] 


Int x = 0;
Int y = 0;
Int z = 1;
While (x == y) do { If (x == 5) then{ x := x + 1; }
								else{ x := x + 1; 
									  y := y + 1; }
					Int z = z * (x * y);}
						^
						|
start [Declare ("x", 0), Declare ("y", 0), Declare ("z", 1), While (Operation Eq (Symbol "x") (Symbol "y")) (Composition [If (Operation Eq (Symbol "x") (Value 5)) [Assign "x" (Operation Add (Symbol "x") (Value 1)), (Composition ([Assign "x" (Operation Add (Symbol "x") (Value 1)), Assign "y" (Operation Add (Symbol "y")  (Value 1))]))], Assign "z" (Operation Multiply (Symbol "z") (Operation Multiply (Symbol "x") (Symbol "y")))])] []

--}