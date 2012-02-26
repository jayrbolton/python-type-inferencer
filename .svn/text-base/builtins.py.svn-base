# All builtin types 

from inftype import *


## Templates for types:
# Numeric
float_typ = Instance("float", float)
int_typ = Instance("int", int)
# Strings
str_typ = Instance("str", str)
# None
none_typ = Instance("None",type(None))
# Booleans
bool_typ = Instance("bool",bool)

env = Environment({
	# Arithmetic
	("*",float_typ,int_typ)  : float_typ,
	("/",float_typ,int_typ)  : float_typ,
	("%",float_typ,int_typ)  : float_typ,
	("//",float_typ,int_typ) : float_typ,
	("+",int_typ,int_typ)    : int_typ,
	("+",int_typ,float_typ)  : float_typ,
	("+",str_typ,str_typ)    : str_typ,

	# Constants
	"None"                   : none_typ,
	"True"                   : bool_typ,
	"False"                  : bool_typ, 

	# IO
	"print"                  : none_typ
})
