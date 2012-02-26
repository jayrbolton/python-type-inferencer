import sys
from ast import *
from builtins import *

"""
TODO
Change all "print_type" methods to "__repr__"

"""


"""
The AnalyzedProgram holds the abstract syntax tree, a type tree, and a type
table. The type trees and type tables hold the same data, but organized
differently for convenience. The Environment class does all the type
inference.

The top level ProgramGraph holds a list of modules
"""

class ProgramGraph:

	modules = []

	def __init__(self,fileName):
		f = open(fileName)
		self.ast = parse(f.read(),filename=fileName)

	def traverse(self, node):
		if isinstance(node, Module):
			[self.modules.append(self.traverse(n)) for n in node.body]
			return Node(node,self.modules,scope=builtins)
		elif isinstance(node, Assign):
			return Node(node)
		elif isinstance(node, Expr):
			return self.traverse(node.value)
		elif isinstance(node, Num):
			t = node.n.__class__.__name__
			return Num(node,t,node.n)
		elif isinstance(node,BinOp):
			l = self.traverse(node.left)
			r = self.traverse(node.right)
			name = node.op.__class__.__name__
			# FuncType() takes syntax_name, typestr, lexical token (name), list of
			# inputs, the output type
			t = FuncType("BinOp","object",name,[l,r],UnknownType())
			t.infer()
			return t
		elif isinstance(node,Str):
			t = node.s.__class__.__name__
			return Name("Str",t,"\"" + node.s + "\"")
		elif isinstance(node,Name):
			i = Name("Name","object",node.id)
			i.infer()
			return i
		elif isinstance(node,If):
			test = self.traverse(node.test)
			body = []
			[body.append(self.traverse(n)) for n in node.body]
			i = ConditionType("If","conditional",test,body)
			return i 
		elif isinstance(node,Lambda):
			body = self.traverse(node.body)
			args = [self.traverse(a) for a in node.args.args]
			t = FuncType("Lambda",body.typestr,"lambda",args,body)
			return t
		else:
			return UnknownType()

	# Print all the environment's type trees as indentation trees.
	def print_modules(self):
		[t.print_type(0) for t in self.modules]

	def dump_ast(self):
		print(dump(self.ast))




"""
The following classes map 1:1 to the AST data structure. These
classes include the AST objects themselves as fields along
with type information.

Single type objects often describe many different types. For example, an
Name could be an int, a str, or any user-defined type. A FuncType could
have an infinite number of type signatures.

All types have a typestr, or type string, field that can be accessed to
always get the typename. They also always store the syntax name, which is given
by the python's parser.

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


class Module(ProgramGraph):
	def __init__(self):
		pass


"""
If statements
These hold the type object of the test expression as well as a list of all the
type objects in the body.
"""

class If(ProgramGraph):
	def __init__(self,ast_node,test,body):
		self.ast_node = ast_node
		self.test = test
		self.body = body

	def print_type(self,indents):
		sys.stdout.write("  "*indents)
		sys.stdout.write("If")
		sys.stdout.write("  "*indents+1)
		print("test = ")
		self.test.print_type(indents+1)
		sys.stdout.write("  "*indents+1)
		print("body = ")
		for b in self.body:
			b.print_type(indents+1)
	
		

"""
Assignments are almost like functions, except they cannot return anything. They
also have an IO side effect of writing to memory, which we note in the type
signature.

The inference rule for Assignments:
	The type of the lhs is the same as that of the rhs

TODO
Infer multiple types on the lhs for an iterable on the rhs
"""
class Assign(ProgramGraph):
	def __init__(self,lhs,rhs):
		self.lhs = lhs # left hand side and right hand side
		self.rhs = rhs
		for n in lhs:
			builtins[n.name] = rhs.typestr
	
	def print_type(self,indents):
		sys.stdout.write("  "*indents)
		sys.stdout.write("Assign (")
		for n in self.lhs:
			sys.stdout.write(n.name + " ")
		print(") : " + self.rhs.typestr)
		self.rhs.print_type(indents+1)



class Unknown(ProgramGraph):
	def __init__(self):
		pass

	def print_type(self,indents):
		sys.stdout.write("  "*indents)
		print("unknown")




class Name(ProgramGraph):
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




"""
This type describes functions which have a list of types for their input
parameters and a single type for their return value
Like instance types, they will have a syntax name from the AST, the name of
their class, and the actual name of the function itself.
"""
class BinOp(ProgramGraph):
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

builtins = {
  	("Mult","float","int") : Name("Num","float"),
  	("Div","float","int") : Name("Num","float"),
  	("Mod","float","int") : Name("Num","float"),
  	("FloorDiv","float","int") : Name("Num","float"),
  	("Add","int","int") : Name("Num","int"),
  	("Add","int","float") : Name("Num","float"),
  	("Add","str","str") : Name("Str","str"),
  	"None" : "NoneType",
  	"True" : "bool",
  	"False" : "bool"
}
