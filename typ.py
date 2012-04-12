"""
Inferred types

The hierarchy:
Type
 Variable
 Object
  Builtin
   List
   Dict
"""

import logging

from substitution import *

class Type:
	"""
	The superclass of all our types.
	"""
	pass

total_variables = 0 ### XXX make this better? globals ew?
class Variable(Type):
	"""
	Type variables. In python's case, they are polymorphic through structural
	subtyping, not parametric polymorphism. 

	The name is a 'fresh,' or previously unused, variable of the form 'tn' where
	'n' is the number of variable types at the time of creation.
	"""

	def __init__(self):
		global total_variables
		self.name = "t" + str(total_variables)
		total_variables += 1

	def __str__(self):
		return self.name

	def __eq__(self, other):
		return self.name == other.name

	def apply_sub(self, sub):
		"""
		If the Substitution for this type variable exists in the provided
		dictionary of Substitutions, then retrieve it, otherwise return self.
		"""
		return sub.subs.get(self.name, self)

	def free_type_vars(self):
		"""
		Returns the set of unbound type variables in this type.
		For single type variables it is simply a singleton of its own name.
		"""
		return set([self.name])

	def unify(self, typ):
		"""
		Unify a type variable (self) with any type (t)
		Attempt to assign a type variable to this type and return that assignment
		as a Substitution.
		"""
		if isinstance(typ, Variable):
			if self.name == typ.name: return Substitution()
			else: return Substitution({self.name : typ})
		else: # typ is not a type variable
			if self.name in typ.free_type_vars(): return Substitution()
		return Substitution({self.name : typ})


class Object(Type):
	"""
	The object type, of which all data is a member in Python. We describe python
	types as encapsulating attributes, and unification involves checking
	corresponding attributes (duck typing).
	"""

	def __init__(self,name,attributes):
		self.name = name
		self.attributes = attributes

	def __str__(self):
		s = self.name
		if self.applied:
			for a in reversed(self.applied): ## XXX inefficient?
				if isinstance(a,Arrow): x = str(a.right)
				else: x = str(a)
				s += "(" + x + ")"
		return s

	def apply_sub(self,sub):
		"""
		Apply a Substitution on a record type.
		Record types are not substitutable, but their attributes may be, so we loop
		through 'attributes' and apply 'sub' to each.

		Does not modify 'this'; returns a new Record object.
		"""
		new_attrs = []
		for each in self.attributes:
			new_attrs.append(each.apply_sub(sub))
		return Record(new_attrs)
		
	def free_type_vars(self):
		"""
		Returns the set of unbound type variables in this type.
		For most instance types, it is trivial: there are no type variables at all.
		For instance types applied to other types, then we recurse on those.
		Returns a list of type names
		"""
		s = set()
		for t in self.applied:
			s.union(t.free_type_vars())
		return s

	def unify(self,typ):
		"""
		Unify an instance type with a another type. The only case in which we can
		create a Substitution is if we are unifying with a type variable.
		"""
		if isinstance(typ, Variable):
			if typ.name in self.free_type_vars(): # occurs check
				return Substitution()
			else:
				return Substitution({typ.name : self}) # sub variable with instance
		# Else if both are the same instance types and have unifiable applied types:
		elif isinstance(typ,Builtin) and self.name == typ.name and self.applied and typ.applied and len(self.applied) == len(typ.applied):
			sub = Substitution({})
			logging.info("initial sub: " + str(sub))
			for (self_applied, other_applied) in zip(self.applied, typ.applied):
				sub.merge(self_applied.unify(other_applied))
				logging.info("self applied = " + str(self_applied))
				logging.info("other applied = " + str(other_applied))
				logging.info("sub loop = " + str(sub))
			return sub
		else:
			return Substitution()

class Builtin(Record):
	def __init__(self,pytype)
		self.pytype = pytype

class List(Builtin):
	pass

class Dict(Builtin):
	pass

class Builtin(Record):


"""
Function application type. Stores input as left and return type as out
e.g.
Add :: (Int, Float) -> Float
"""
class Arrow(Type):
	def __init__(self, left, right):
		"""
		Pass the left and right types for a function.
		In python we assign the left types to a tuple type containing one or more
		parameters.
		"""
		self.left = left
		self.right = right

	def __str__(self):
		return "(" + str(self.left) + " -> " + str(self.right) + ")"

	def apply_sub(self,sub):
		"""
		Simply go down the tree and apply the Substitutions to the left and right
		values of this arrow type.
		"""
		return Arrow(self.left.apply_sub(sub), self.right.apply_sub(sub))

	def free_type_vars(self):
		"""
		Returns the set of unbound type variables in this type.
		For arrow types, it's simply the union of free type vars in the left and
		right subtrees of this type.
		"""
		return self.left.free_type_vars().union(self.right.free_type_vars())

	def unify(self, typ):
		"""
		Unify this arrow type with another arrow type.  We first unify the two
		types on the left. From this unification we get back a new Substitution
		that we will apply to the two types on the right sides.  Then we do the
		unification of those Substitutions, which will return yet another
		Substitution, which we'll combine back into sub1 (and we return sub1).
		"""
		if isinstance(typ, Variable):
			if typ.name in self.free_type_vars(): return Substitution()
			else: return Substitution({typ.name : self})
		elif isinstance(typ, Arrow):
			s1 = self.left.unify(typ.left)
			s2 = self.right.unify(typ.right)
			logging.info("For typ = " + str(typ))
			logging.info("For self = " + str(self))
			logging.info("Merging s1 (" + str(s1) + ") and s2 (" + str(s2) + ")")
			s1.merge(s2)
			logging.info("Merged s1 and s2: " + str(s1))
			return s1
		else: return Substitution()
