"""
Inferred types

The hierarchy:
Type
 TVar
 TObj
  Builtin
   List
"""

import logging

from substitution import *
from attributes import *

class Type(object):
	"""
	The superclass of all our types.
	"""
	pass

class TObj(Type):
	"""
	The object type, of which all data is a member in Python. We describe python
	types as encapsulating attributes, and unification involves checking
	corresponding attributes (duck typing).
	"""

	def __init__(self,attributes=None):
		"""
		Pass a dict to the constructor to TObj of the mapping of names to types in the attributes of this object.
		"""
		if attributes == None: self.attributes = Attributes({})
		else: self.attributes = Attributes(attributes)

	def __str__(self): return str(self.attributes)
	def __repr__(self): return str(self.attributes)

##def apply_sub(self,sub):
##	"""
##	Apply a type Substitution to an object.
##	TObjs themselves are not substitutable, but their attributes may be, so we loop
##	through 'attributes' and apply 'sub' to each.

##	Does not modify 'this'
##	-> Returns a new TObj with subs applied
##	"""
##	for name, typ in self.attributes.iteritems():
##		self.attributes[name] = typ.apply_sub(sub)
		
	def free_type_vars(self):
		"""
		Returns the set of unbound type variables in this type.
		For object types, this is a matter of finding any free type variables in
		its attributes. The object itself can never be a type variable.
		-> Returns a list of type names
		"""
		s = set()
		s.union(self.name)
		for name, typ in self.attributes.iteritems():
			s.union(name)
			s.union(typ.free_type_vars())
		return s

	def unify(self,typ):
		"""
		Unify an object type with a another type. The only case in which we can
		create a Substitution is if we are unifying with a type variable.
		"""
		return TObj(self.attributes.unify(typ.attributes))

## XXX TODO inherit attributes
class TError(TObj):
	attributes = {}
	def __init__(self,message): self.message = message
	def __str__(self): return "<<Type Error: " + self.message + ">>"
	def __repr__(self): return "<<Type Error: " + self.message + ">>"

class TBuiltin(TObj):
	def __init__(self,pytype,attributes):
		self.pytype = pytype
		self.attributes = attributes

	def __str__(self):
		return str(self.pytype) + " " + super(TBuiltin,self).__str__()
	def __repr__(self):
		return str(self.pytype) + " " + super(TBuiltin,self).__str__()

	def unify(self,typ):
		if self.attributes == typ.attributes: return self
		elif isinstance(typ,TObj) and not typ.attributes: return self
		else: return TError("Conflicting types: " + str(self) + " and " + str(typ))

class TTuple(TBuiltin):
	pytype = tuple
	attributes = {}
	def __init__(self,contained): self.contained = contained
	def __str__(self): return str(self.contained)
	def __repr__(self): return str(self.contained)

class TList(TBuiltin):
	pytype = list
	def __init__(self,contained): self.contained = contained

class TDict(TBuiltin):
	pytype = dict
	def __init__(self,contained): self.contained = contained
