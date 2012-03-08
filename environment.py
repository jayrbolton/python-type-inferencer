
from program_graph import *

"""
An Environment is a dictionary of names and their type schemes. Names are
syntactic names derived from the AST tree, such as variables, literals,
primitives, function names, class names, and so forth.
"""
class Environment:
	def __init__(self, types):
		self.types = types

	def __repr__(self):
		s = "{"
		for typ, sig in self.types.iteritems():
			s += str(typ)
			s += " : "
			s += str(sig)
			s += ", "
		s += "}\n"
		return s


	def bind(self, v, t):
		"""
		Replace the binding for the variable 'v' in this environment with the
		type 't'.
		Returns this environment.
		"""
		existing = self.types.get(v)
		if existing:
			if existing == t:
				return Substitution()
			if isinstance(existing, Instance) and existing.applied: ## XXX relies on short circuiting
				self.types[v] = Instance("tuple",tuple,existing.applied + [t])
			else:
				self.types[v] = Instance("tuple",tuple,[existing] + [t])
		else:
			self.types[v] = t
		return self

	def merge(self, env2):
		"""
		Merge the mapping of this environment with another.
		For overlapping entries, we create union types. (For example, if a variable
		is later reinitialized as a different type, that variable is given both
		types.)
		1. Loop through env2.types and check each key.
		1a. If the type is already in self.types, then add env2's type to self's type as a list of types.
		1b. If the type is not in self.types, then simply add it.
		Returns this environment
		"""
		for each_name in env2.types.keys(): # 1.
			entry = self.types.get(each_name)
			if entry: # 1a. TODO the logic below could def be more elegant/less redundant/less ugly
				if env2.types.get(each_name) == entry:
					pass
				elif isinstance(entry, list): # already a list
					self.types[each_name] = Instance("tuple",tuple,entry + [env2.types[each_name]])
				else:
					self.types[each_name] = Instance("tuple",tuple,[entry] + [env2.types[each_name]])
			else: # 1b.
				self.types[each_name] = env2.types[each_name]
		return self

	# apply s   (TypeEnv env) =  TypeEnv   $ Map.map (apply s) env
	def apply_sub(self,subst):
		"""
		Apply the substitution to every value in the types dictionary.
		(In other words, apply 'subst' to every type in the environment)
		"""
		for each_type in self.types.values(): each_type.apply_sub(subst)
		return self

	def free_type_vars(self):
		"""
		Return the set of free type variables in the whole environment.
		"""
		s = []
		for each_type in self.types.values():
			s.append(each_type.free_type_vars())
		return set(s)
