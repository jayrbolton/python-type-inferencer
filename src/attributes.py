"""
An Attributes is a dictionary of names and their type schemes. Names are
syntactic names derived from the AST tree, such as variables, literals,
primitives, function names, class names, and so forth.
"""

from substitution import *

total_vars = 0 ### Generator of fresh names. XXX make this better? globals ew?
class Attributes(object):
	def __init__(self, attrs=None):
		self.attrs = {}
		if attrs: self.attrs = attrs

	def __str__(self): return str(self.attrs)

	def add_type(self, t, name=None):
		if name == None:
			global total_vars
			n = "object" + str(total_vars)
			total_vars += 1
		else: n = name
		self.attrs[n] = t

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
				sub.merge(typ1.unify(typ2))
		return sub

	def reference(self, name, typ): pass

	def apply_sub(self,sub):
		"""
		Apply the subitution to every type in these attributes
		"""
		new_attrs = {}
		for name,each_type in self.attrs.iteritems():
			new_attrs[name] = each_type.apply_sub(sub)
		self.attrs = new_attrs
		return self

	def free_type_vars(self):
		"""
		Return the set of free type variables in the whole environment.
		"""
		s = []
		for each_type in self.attrs.itervalues(): s.append(each_type.free_type_vars())
		return set(s)
