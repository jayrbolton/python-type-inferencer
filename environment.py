
from program_graph import *

"""
An Environment is a dictionary of names and their type schemes. Names are
syntactic names derived from the AST tree, such as variables, literals,
primitives, function names, class names, and so forth.
"""
total_vars = 0 ### Generator of fresh names. XXX make this better? globals ew?
class Environment:
	def __init__(self, types):
		self.types = types

	def __str__(self): return str(self.types)

	def add_type(self, t, name=None):
		if name == None:
			global total_vars
			n = "object" + str(total_vars)
			total_vars += 1
		else: n = name
		self.types[n] = t

	def merge(self, env2): self.types.update(env2.types)

	def apply_sub(self,subst):
		"""
		Apply the substitution to every value in the types dictionary.
		(In other words, apply 'subst' to every type in the environment)
		"""
		for each_type in self.types.itervalues(): each_type.apply_sub(subst)
		return self

	def free_type_vars(self):
		"""
		Return the set of free type variables in the whole environment.
		"""
		s = []
		for each_type in self.types.itervalues(): s.append(each_type.free_type_vars())
		return set(s)
