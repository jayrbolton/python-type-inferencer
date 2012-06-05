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

from .. import substitution as subst
from .. import attributes as attr

class Type(object):
	"""
	The superclass of all our types.
	"""
	pass

total_vars=0
class TObj(Type):
	"""
	The object type, of which all data is a member in Python. We describe python
	types as encapsulating attributes, and unification involves checking
	corresponding attributes (duck typing).
	"""

	def __init__(self,attributes,label=None):
		"""
		Pass a dict to the constructor to TObj of the mapping of names to types in the attributes of this object.
		"""
		self.attributes = attr.Attributes(attributes)
		self.open_type = False
		if label == None:
			global total_vars
			self.label = "t" + str(total_vars)
			total_vars += 1
		else: self.label = label

	def __str__(self): return str(self.label) + str(self.attributes)
	def __repr__(self): return str(self.label) + str(self.attributes)

	def get_attr(self,name): return self.attributes.get_type(name)
	def add_attr(self,t,name): self.attributes.add_type(t,name)

	def apply_sub(self,sub):
		if sub.subs:
			mysub = sub.subs.get(self.label)
			if mysub:
				self = mysub
			else:
				subbed = {}
				for name, typ in self.attributes.attrs.iteritems():
					self.attributes.attrs[name] = typ.apply_sub(sub)
		return self

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
		Unify an object type with a another type. There are four cases:
		1. If both are empty type objects, don't bother to substitute anything.
		2. If self is an empty type object, substitute it with anything.
		3. If self is not empty and typ is a non-empty type object, unify the attributes.
		4. Otherwise, substitute this type for a type error.
		-> Returns a Substitution.
		"""
		if not self.attributes.attrs:
			return subst.Substitution({self.label : typ})
		elif isinstance(typ,TObj):
			if not typ.attributes.attrs: return subst.Substitution({typ.label : self})
			return self.attributes.unify(typ.attributes)
		else:
			err = TError("Conflicting types: " + str(self) + " and " + str(typ))
			return subst.Substitution({self.label : err})

## XXX TODO inherit attributes
class TError(TObj):
	attributes = attr.Attributes({'x':1})
	def __init__(self,message): self.message = message
	def __str__(self): return "<<Type Error: " + self.message + ">>"
	def __repr__(self): return "<<Type Error: " + self.message + ">>"
	def apply_sub(self,sub): return self

class TBuiltin(TObj):
	label = "builtin"
	attributes = attr.Attributes({'x':1})
	def __init__(self,pytype): self.pytype = pytype

	def __str__(self): return str(self.pytype)
	def __repr__(self): return str(self.pytype)

	def unify(self,typ):
		"""
		Builtins are not unifiable. There are three cases:
		1. self and typ are the same builtin types, in which case don't bother to substitute.
		2. typ is a an empty type object, in which case don't bother to substitue
		3. otherwise substitute a type error.
		"""
		if isinstance(typ,TObj) and not typ.attributes.attrs:
			return subst.Substitution({typ.label : self})
		if self.__class__ == typ.__class__:
			return subst.Substitution()
		else:
			err = TError("Conflicting types: " + str(self) + " and " + str(typ))
			return subst.Substitution({self.label : err})

	def apply_sub(self,sub): return self

class TTuple(TBuiltin):
	pytype = tuple
	attributes = attr.Attributes({'x':1})
	def __init__(self, contained):
		self.contained = contained
		global total_vars
		self.label = "tuple" + str(total_vars)
		total_vars += 1
	def __str__(self): return str(self.label) + str(self.contained)
	def __repr__(self): return str(self.label) + str(self.contained)

	def unify(self,typ):
		if isinstance(typ,TObj) and not typ.attributes.attrs: return subst.Substitution()
		elif isinstance(typ,TTuple):
			sub = subst.Substitution()
			if len(self.contained) == len(typ.contained):
				for t1, t2 in zip(self.contained,typ.contained):
					sub.merge(t1.unify(t2))
				return sub
			else:
				err = TError("Conflicting types: " + str(self) + " and " + str(typ))
				return subst.Substitution({self.label : err})
		err = TError("Conflicting types: " + str(self) + " and " + str(typ))
		return subst.Substitution({self.label : err})

	def apply_sub(self,sub):
		if sub.subs:
			mysub = sub.subs.get(self.label)
			if mysub: self = mysub
			else:
				self.contained = [c.apply_sub(sub) for c in self.contained]
		return self


class TList(TBuiltin):
	label = "list"
	pytype = list
	def __init__(self,contained): self.contained = contained
	def apply_sub(self,sub):
		t = TList([c.apply_sub(sub) for c in self.contained])
		return t

class TDict(TBuiltin):
	label = "dict"
	pytype = dict
	def __init__(self,contained): self.contained = contained
	def apply_sub(self,sub): return self

class TSelf(TBuiltin):
	label = "self"
	pytype = object

	def __init__(self,attrs=None):
		if attrs == None: self.attributes = attr.Attributes({})
		else: self.attributes = attr.Attributes(attrs)

	def apply_sub(self,sub): return self
	def __repr__(self): return "s" + str(self.attributes)
	def __str__(self): return "s" + str(self.attributes)
