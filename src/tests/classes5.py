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

# Undefined attributes inside function application
def f(x): return x.quack
e = f(a)
