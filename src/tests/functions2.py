

# Returning a function object
def f(): return hi # : 'hi' is undefined

# Function application to parameters in the body changes the type of the parameters.

def S(x,y):  return x      # : (a{}, b{}) -> a{}
def S2(x,y): return S(x,y) # : (a{}, b{}) -> a{}

a = S("s",2)      # : str
b = S2(2,"s")     # : int
#c = S(S2,S)       # : type of S2
