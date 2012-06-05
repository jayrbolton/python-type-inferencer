
# Basic
def hi(y,z): # : (a{}, b{}) -> str
	"""
	This is a really amazing docstring
	"""
	return "hi"

a = hi(1,2)       # : str

# Shadowing: shadow n as a parameter
n = 4 # : int

def shadow(n): # : (a{}) -> a{}
	return n

b = shadow("ret") # : str

n # : int

# Type errors:
# Parameters too many or few:
e1 = hi(1,2,3) # : error: conflicting params
e2 = hi(1)     # : error: conflicting params
