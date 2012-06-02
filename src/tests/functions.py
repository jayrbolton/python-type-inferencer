
# Basic
def hi(y,z): # : (a{}, b{}) -> str
	"""
	This is a really amazing docstring
	"""
	return "hi"

# Shadowing: shadow n as a parameter
n = 4 # : int

def shadow(n): # : (a{}) -> a{}
	return n

n # : int

# Returning a function object
def f(): return hi # : () -> ((a{}, b{}) -> str)

# Multiple return types

# def multi(p):
# 	if p: return 1
# 	else: return 2

# Function application to parameters in the body changes the type of the parameters.

def S(x,y):  return x      # : (a{}, b{}) -> a{}
def S2(x,y): return S(x,y) # : (a{}, b{}) -> a{}

# Function calls:

a = hi(1,2)       # : str
b = shadow("ret") # : str
c = S("s",2)      # : str
c = S2(2,"s")     # : int
d = S(hi,shadow)  # : t3{...} (hi function type)

# Type errors:
# Parameters too many or few:
hi(1,2,3) # : error: conflicting params
hi(1)     # : error: conflicting params
