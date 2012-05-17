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

class Type:
	"""
	The superclass of all our types.
	"""
	pass


total_vars = 0 ### Generator of fresh names. XXX make this better? globals ew?
class TObj(Type):
	"""
	The object type, of which all data is a member in Python. We describe python
	types as encapsulating attributes, and unification involves checking
	corresponding attributes (duck typing).
	"""

	def __init__(self,attributes,name=None):
		if name == None:
			global total_variables
			self.name = "o" + str(total_variables)
			total_variables += 1
		else:
			self.name = name
		self.attributes = attributes


	def __str__(self):
		s = self.name
		if self.attributes:
			s += "["
			for a in self.attributes: s += " " + str(a) + " "
			s += "]"
		return s

	def apply_sub(self,sub):
		"""
		Apply a type Substitution to an object.
		TObjs themselves are not substitutable, but their attributes may be, so we loop
		through 'attributes' and apply 'sub' to each.

		Does not modify 'this'
		-> Returns a new TObj with subs applied
		"""
		new_attrs = []
		for each in self.attributes:
			new_attrs.append(each.apply_sub(sub))
		return TObj(new_attrs)
		
	def free_type_vars(self):
		"""
		Returns the set of unbound type variables in this type.
		For object types, this is a matter of finding any free type variables in
		its attributes. The object itself can never be a type variable.
		-> Returns a list of type names
		"""
		s = set()
		s.union(self.name)
		for a in self.attributes:
			s.union(a.free_type_vars())
		return s

	def unify(self,typ):
		"""
		Unify an object type with a another type. The only case in which we can
		create a Substitution is if we are unifying with a type variable.
		"""
		if isinstance(typ, TVar):
			if typ.name in self.free_type_vars(): # occurs check
				return Substitution() # failed occurs check; ret empty sub
			else:
				return Substitution({typ.name : self}) # sub variable with this object
		# Else if both are object types and have unifiable names and attributes.
		elif isinstance(typ,TObj):
			sub = Substitution({self.attributes.extend})
			return sub
		else:
			return Substitution()

class TBuiltin(TObj):
	def __init__(self,pytype,name):
		self.pytype = pytype
		self.name = name

class TList(TBuiltin):
	pass

class TDict(TBuiltin):
	pass
