# All builtin types
# http://docs.python.org/2/library/stdtypes.html

from types.typ import *
from attributes import *

## Templates for types:
# Numeric
float_typ = TBuiltin(float)
int_typ = TBuiltin(int)
# Strings
str_typ = TBuiltin(str)
# None
none_typ = TBuiltin(type(None))
# Booleans
bool_typ = TBuiltin(bool)
self_typ = TSelf()

env = Attributes({
# "+" : Attributes({"*params":	...
	})
#	# Arithmetic
#	("*",float_typ,int_typ)  : float_typ,
#	("/",float_typ,int_typ)  : float_typ,
#	("%",float_typ,int_typ)  : float_typ,
#	("//",float_typ,int_typ) : float_typ,
#	("+",int_typ,int_typ)    : int_typ,
#	("+",int_typ,float_typ)  : float_typ,
#	("+",str_typ,str_typ)    : str_typ,
#
#	# Constants
#	"None"                   : none_typ,
#	"True"                   : bool_typ,
#	"False"                  : bool_typ,
#
#	# IO
#	"print"                  : none_typ
#})
