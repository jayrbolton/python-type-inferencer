# Class definition

class A(object):
	# Assignment attributes
	z = 1

	def __init__(self,x):
		self.x = x
		self.y = "str"
		self.n = 1

	# Operator overloading
	def __add__(self,n): return n

	# Static methods	
	def smethod(p1): return p1 # : (a{}) -> a{}

	# Instance methods
	def imethod(self): return self # : (A{...}) -> A{...}

# Construction

a = A() # : A{...}

# Attribute reference

y = a.z # : int

# Static method reference

z = A.smethod(1)

# Instance method reference

z = a.imethod()

# Reference of attributes in functions
def g(x) = x.z
g(a) # : int

## Type errors:

# Undefined attributes
a.wat
A.wat
a.smethod()
A.imethod()

def f(x): x.quack
f(a)
