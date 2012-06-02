## Demo.py --- a demonstration of python type inference
## Jay R Bolton
#

x = y # type error: undefined
x = 1
y = "hi"

def S(x,y): return x

q = S(1,"hi")

def S2(x,y): return S(x,y)

## Assignment and primitives
#x = y ## type error: y undefined
#y = 1
#z = y
#y = "str"
#
### Basic function definition
#
## Should have type equivalent to (t0,t1)->t0
## Type of parameter x will shadow global x
#def S(x,y):  return x 
#
## return a function object
#def f(): return S
#
## take a function object and apply it
#def g(x,y,func): return func(x,y)
#
#def S2(x,y): return S(x,y)
#
### Function calls
#
#q = S(z,"hi") ## Type should infer to int
#q = S(z) ## Error: conflicting parameters
#q = S(x,x) ## X is still undefined
#q = S(y,z,x) ## Error: conflicing parameters
#
#s = f()
#r = g("hi",42,S)
#
#q = S(1,"hi")
#
### Class definition
#
#class A(object):
#	z = 1
#	def static(p1, p2):
#		return S(p1,p2)
#	def instance(p1,p2):
#		return S("str",1)
#
### Construction
#
#a = A()
#
### Attribute reference
#
#y = a.z
#
### Static method reference
#
#z = a.static(1,2)
