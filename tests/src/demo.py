## Demo.py --- a demonstration of python type inference
## Jay R Bolton

## Assignment and primitives
x = y ## type error: y undefined
y = 1
z = y
y = "str"

## Function definition

# Should have type equivalent to (t0,t1)->t0
# Type of parameter x will shadow global x
def S(x,y):  return x 

# return a function object
def f(): return S

# take a function object and apply it
def g(x,y,func): return func(x,y)

## Function calls

q = S(y,z) ## Type should infer to int
q = S(z) ## Error: conflicting parameters
q = S(x,x) ## X is still undefined
q = S(y,z,x) ## Error: conflicing parameters

s = f()
r = g("hi",42,S)

## Class definition

class A(object):
	z = 1

a = A()

## Attribute reference
