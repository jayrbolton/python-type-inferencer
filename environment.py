
from program_graph import *

"""
An Environment is a dictionary of names and their type schemes. Names are
syntactic names derived from the AST tree, such as variables, literals,
primitives, function names, class names, and so forth.
"""
class Environment:
	def __init__(self, types):
		self.types = types

	def __str__(self):
		s = "{"
		for typ in self.types: s += str(typ) + ", "
		s += "}\n"
		return s

	def add_type(self, t): self.types.append(t)

	def merge(self, env2): return self.extend(env2)

	def apply_sub(self,subst):
		"""
		Apply the substitution to every value in the types dictionary.
		(In other words, apply 'subst' to every type in the environment)
		"""
		for each_type in self.types: each_type.apply_sub(subst)
		return self

	def free_type_vars(self):
		"""
		Return the set of free type variables in the whole environment.
		"""
		s = []
		for each_type in self.types: s.append(each_type.free_type_vars())
		return set(s)
