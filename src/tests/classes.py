# Class definition

class A(object):
	# Assignment attributes
	z = 1

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

## Type errors:

# Undefined attributes
a.wat
A.wat
a.smethod()
A.imethod()

