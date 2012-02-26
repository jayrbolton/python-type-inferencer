"""
Type objects for python. 

The goal is to be as general and abstract as possible.

Single type objects often describe many different types. For example, an
InstanceType could be an int, a str, or any user-defined type. A FuncType could
have an infinite number of type signatures.

All types have a typestr, or type string, field that can be accessed to
always get the typename. They also always store the syntax name, which is given
by the python's parser.

Called 'pytypes.py' to not conflict with lib/types.py
"""

"""
TODO
Change all "print_type" methods to "__repr__"

"""

"""
	The scope hierarchy:
	Library (a list of modules): builtins
		Module: globals
			Class: the class' fields and methods
				Method: vars within a func def
					Nested methods: vars within a func within a func etc
					Loops: loop vars
"""


class Type:
	type_scope = builtins
	program = [] # a list of modules



"""
Scope Objects
"""

"""

"""
class ModuleScope(Type):
	def __init__(self):
		pass


"""
If statements
These hold the type object of the test expression as well as a list of all the
type objects in the body.
"""
class ConditionType(Type):
	def __init__(self,syntax_name,typestr,test,body):
		self.typestr = typestr
		self.test = test
		self.body = body

	def print_type(self,indents):
		sys.stdout.write("  "*indents)
		sys.stdout.write("if : ")
		print(self.typestr)
		sys.stdout.write("  "*indents)
		print("test = ")
		self.test.print_type(indents+1)
		sys.stdout.write("  "*indents)
		print("body = ")
		[b.print_type(indents+1) for b in self.body]
	
		

"""
Assignments are almost like functions, except they cannot return anything. They
also have an IO side effect of writing to memory, which we note in the type
signature.

The inference rule for Assignments:
	The type of the lhs is the same as that of the rhs

TODO
Infer multiple types on the lhs for an iterable on the rhs
"""
class AssignType(Type):
	def __init__(self,lhs,rhs):
		self.lhs = lhs # left hand side and right hand side
		self.rhs = rhs
		for n in lhs:
			builtins[n.name] = rhs.typestr
	
	def print_type(self,indents):
		sys.stdout.write("  "*indents)
		sys.stdout.write("Assign (")
		[sys.stdout.write(n.name + " ") for n in self.lhs]
		print(") : " + self.rhs.typestr)
		self.rhs.print_type(indents+1)



class UnknownType(Type):
	def __init__(self):
		self.name = "object"
		self.typestr = "object"

	def print_type(self,indents):
		sys.stdout.write("  "*indents)
		print("object")


# Instance types constitute the leaves of the type tree and include such things
# as numbers, strings (all primitive types), and instances of objects.
# Their type is described by their typestr
# The syntax_name is their AST object
# Ther name is their actual lexical token string (such as "1" or "wat")
class InstanceType(Type):
	def __init__(self,syntax_name,typestr,name=None):
		self.syntax_name = syntax_name
		self.typestr = typestr
		if name: 
			self.name = str(name)
		else:
			self.name = typestr

	def print_type(self,indents):
		sys.stdout.write("  "*indents)
		print(self.name + " : " + self.typestr)

	def infer(self):
		try:
			q = builtins[self.name]
		except:
			q = False
		if q:
			self.typestr = q
		return self.typestr




# This type describes functions which have a list of types for their input
# parameters and a single type for their return value
# Like instance types, they will have a syntax name from the AST, the name of
# their class, and the actual name of the function itself.
class FuncType(Type):
	def __init__(self,syntax_name,typestr,name,inputs,output):
		self.syntax_name = syntax_name
		self.typestr = typestr
		self.name = name
		self.inputs = inputs
		self.output = output
		self.output.name = "output"

	def print_type(self,indents):
		sys.stdout.write("  "*indents)
		sys.stdout.write(self.name + " : ")
		[sys.stdout.write(it.typestr + "->") for it in self.inputs]
		print(self.output.typestr)
		[t.print_type(indents+1) for t in self.inputs]
		self.output.print_type(indents+1)

	def infer(self):
		params = [self.name]
		[params.append(i.typestr) for i in self.inputs]
		t = tuple(params)
		try:
			q = builtins[t]
		except:
			q = False
		if q:
			self.output = q
			self.output.name = "output"
			self.typestr = self.output.typestr
		return self.typestr
