# All builtin types

from program_graph import *
from typ import *
from environment import *

## Templates for types:
# Numeric
float_typ = Builtin("float", float)
int_typ = Builtin("int", int)
# Strings
str_typ = Builtin("str", str)
# None
none_typ = Builtin("None",type(None))
# Booleans
bool_typ = Builtin("bool",bool)

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
