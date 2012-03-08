# Should have type: (t0, t1) -> str
def x(y,z):
	return "hi"

# Should have type: int
flops = 4

# Flops should be shadowed below:
# Should have type: t0 -> t0
def giga(flops):
	return flops

# The S combinator
# Should have type (t0, t1) -> t0
def S(x,y):
	return x
 
# hack the gibson with higher order functions
# Should have type: (t2, t3) -> ((t0, t1) -> t0)
def hack(the, gibson):
	return S

# Function calling

S(1,"hi")

hack(1,2)

giga("infinity")

x(None, False)

## Now let's play with classes

class A:
	x = lambda x: x+1
	y = B()

class B:
	y = A()
	z = C()

class C:
	x = A()
	Z = "penguins"

a = A()
b = B()
c = C()
