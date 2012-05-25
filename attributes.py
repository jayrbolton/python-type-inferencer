import typ
from program_graph import *
from substitution import *

"""
An Attributes is a dictionary of names and their type schemes. Names are
syntactic names derived from the AST tree, such as variables, literals,
primitives, function names, class names, and so forth.
"""
total_vars = 0 ### Generator of fresh names. XXX make this better? globals ew?
class Attributes(object):
	def __init__(self, attrs): self.attrs = attrs # Dictionary mapping of names to attrs

	def __str__(self): return str(self.attrs)

	def add_type(self, t, name=None):
		if name == None:
			global total_vars
			n = "object" + str(total_vars)
			total_vars += 1
		else: n = name
		self.attrs[n] = t
		logging.debug("Env: " + str(self))

	def get_type(self, name): return self.attrs.get(name)

	def merge(self, a2): self.attrs.update(a2.attrs)

	def unify(self, a2):
		"""
		Unify all the types in these attributes with those in attributes a2.
		-> Returns a Substitution
		"""
		sub = Substitution() # initialize empty substitution
		for name, typ1 in self.attrs.iteritems():
			typ2 = a2.attrs.get(name)
			if typ2:
				logging.debug("Unifying " + str(name) + ": " + str(typ1) + " with " + str(typ2))
				sub.merge(typ1.unify(typ2))
				logging.debug("New substitution: " + str(sub))
		return sub

	def reference(self, name, typ): pass

	def apply_sub(self,subst):
		"""
		Apply the substitution to every type in these attributes
		"""
		for each_type in self.attrs.itervalues():
			each_type.apply_sub(subst)

	def free_type_vars(self):
		"""
		Return the set of free type variables in the whole environment.
		"""
		s = []
		for each_type in self.attrs.itervalues(): s.append(each_type.free_type_vars())
		return set(s)
