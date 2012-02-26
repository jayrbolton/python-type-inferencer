"""
Inferred types
"""

import logging

class Type:
	pass

"""
The unknown type. This type may be polymorphic in some languages, but in python
it's just unknown.

The name is a 'fresh,' or previously unused, variable of the form 'tn' where
'n' is the number of variable types at the time of creation.
"""
total_variables = 0 ### XXX make this better.
class Variable(Type):
	def __init__(self):
		global total_variables
		self.name = "t" + str(total_variables)
		total_variables += 1

	def __repr__(self):
		return self.name

	def __eq__(self, other):
		return self.name == other.name

	def apply_subst(self, subst):
		"""
		If the substitution for this type variable exists in the provided
		dictionary of substitutions, then retrieve it, otherwise return self.
		"""
		return subst.subs.get(self.name, self)

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
		as a substitution.
		"""
		if isinstance(typ, Variable):
			if self.name == typ.name:
				logging.info("Variables with the same name. Returning empty substitution")
				return Substitution()
			else:
				logging.info("Substituting different variables.")
				return Substitution({self.name : typ})
		else: # typ is not a type variable
			if self.name in typ.free_type_vars():
				return Substitution()
		return Substitution({self.name : typ})


"""
The Monotype, such as Int, bool, etc.
The applied field allows for type application:
	e.g. list(str)
			 list(union(str tuple(boolean none) float))
"""
class Instance(Type):
	def __init__(self, name, pytype=None, applied=[]):
		"""
		Pass a string name and the python type object for this instance.
		"""
		self.name = name
		self.pytype = pytype
		self.applied = applied

	def __repr__(self):
		s = self.name
		if self.applied:
			for a in reversed(self.applied): ## XXX inefficient?
				if isinstance(a,Arrow): x = str(a.right)
				else: x = str(a)
				s += "(" + x + ")"
		return s

	def apply_subst(self,sub):
		"""
		Apply a subitution on an instance type.
		Instance types are not subitutable so we do nothing.
		"""
		if self.applied:
			new_applied = []
			for each in self.applied:
				new_applied.append(each.apply_subst(sub))
			return Instance(self.name, self.pytype, new_applied)
		else: return self

	def free_type_vars(self):
		return set([])

	def free_type_vars(self):
		"""
		Returns the set of unbound type variables in this type.
		For most instance types, it is trivial: there are no type variables at all.
		For instance types applied to other types, then we recurse on those.
		Returns a list of type names
		"""
		s = []
		for t in self.applied:
			s.append(t.free_type_vars())
		return set(s)

	def unify(self,typ):
		"""
		Unify an instance type with a another type. The only case in which we can
		create a substitution is if we are unifying with a type variable.
		"""
		if isinstance(typ, Variable):
			if typ.name in self.free_type_vars():
				return Substitution()
			else: return Substitution({typ.name : self})
		## Else if both instances are the same applied types.
		elif isinstance(typ,Instance) and self.name == typ.name and self.applied and typ.applied and len(self.applied) == len(typ.applied):
			sub = Substitution()
			for (self_applied, other_applied) in zip(self.applied, typ.applied):
				sub.merge(self_applied.unify(other_applied))
			return sub
		else: return Substitution()


"""
Function application type. It really just contains instance types.
e.g.
Add :: Int -> Float -> Float
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

	def __repr__(self):
		return "(" + str(self.left) + " -> " + str(self.right) + ")"

	def apply_subst(self,subst):
		"""
		Simply go down the tree and apply the substitutions to the left and right
		values of this arrow type.
		"""
		return Arrow(self.left.apply_subst(subst), self.right.apply_subst(subst))

	def free_type_vars(self):
		"""
		Returns the set of unbound type variables in this type.
		For arrow types, it's simply the union of free type vars in the left and
		right subtrees of this type.
		"""
		free_left = self.left.free_type_vars()
		free_right = self.right.free_type_vars()
		return free_left.union(free_right)

	def unify(self, typ):
		"""
		Unify this arrow type with another arrow type.  We first unify the two
		types on the left. From this unification we get back a new substitution
		that we will apply to the two types on the right sides.  Then we do the
		unification of those substitutions, which will return yet another
		substitution, which we'll combine back into sub1 (and we return sub1).
		"""
		if isinstance(typ, Variable):
			if typ.name in self.free_type_vars():
				return Substitution()
			else: return Substitution({typ.name : self})
		elif isinstance(typ, Arrow):
			s1 = self.left.unify(typ.left)
			s2 = self.right.unify(typ.right)
			logging.info("Merging s1 (" + str(s1) + ") and s2 (" + str(s2) + ")")
			s1.merge(s2)
			logging.info("Merged s1 and s2: " + str(s1))
			return s1
		else: return Substitution()


"""
A list of type variables and a single type.
A quantified type.
e.g. Forall a. a -> b -> c
     where 'a' is a bound variable in the type (a->b->c)
"""
class Scheme:
	def __init__(self, variables, typ):
		self.variables = variables
		self.typ = typ
		self.new_subst = None

	def apply_subst(self, subst):
		"""
		Apply a substitution dictionary to this scheme.
		In the case of Schemes, we introduce a new scope/context so we have to
		create a new Substitution which is the parent substitution minus any new
		bound type variables. This can be compared to variable shadowing in a new
		scope.
		For example, if the type variable 'a' is in the global substitution
		dictionary, but then we have the scheme 'Forall a. a -> b -> c', then the
		'Forall a' is not the same as the global 'a', so we need to remove that
		from the context.
		"""
		self.new_subst = subst
		for v in self.variables:
			if v in self.new_subst.subs: del self.new_subst.subs[v]
		self.typ = self.typ.apply_subst(self.new_subst)

	def free_type_vars(self):
		"""
		Returns the set of unbound type variables in this scheme.
		For a scheme, the free type variables are all the type variables in the
		type minus the quantified variables.
		"""
		type_vars = typ.free_type_vars()
		bound_vars = self.variables
		return type_vars.difference(bound_vars)

	def instantiate(self):
		"""
		Take a quantified/generalized type and instantiate with fresh variables so
		that it no longer needs to be quantified.
		instantiate (Forall as t) = do as' <- mapM (\ _ -> freshTVar "a") as
		                               let s = Map.fromList $ zip as as'
		                               return $ apply s t
		"""
		fresh = []
		for var in self.variables:
			fresh.append(Variable())
		sub = Substitution(self.variables, fresh)
		return self.typ.apply_subst(sub)


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
	def apply_subst(self,subst):
		"""
		Apply the substitution to every value in the types dictionary.
		(In other words, apply 'subst' to every type in the environment)
		"""
		for each_type in self.types.values(): each_type.apply_subst(subst)
		return self

	def free_type_vars(self):
		"""
		Return the set of free type variables in the whole environment.
		"""
		s = []
		for each_type in self.types.values():
			s.append(each_type.free_type_vars())
		return set(s)

"""
A substitution is a mapping of type variables to actual types.
	e.g. { "t1" : "int",
	       "t2" : "t1 -> str"}
The 'vars_to_types' field holds this mapping.
"""
class Substitution:
	def __init__(self, subs={}):
		self.subs = subs
	
	def __repr__(self):
		s = "{"
		for (key,val) in self.subs.iteritems():
			s += str(key) + " : " + str(val) + ","
		s += "}"
		return s

	def merge(self,other_sub):
		self.subs.update(other_sub.subs)
		return self

	def apply_after(self, sub2):
		"""
		Compose two substitutions, sub2 and self.
			e.g. self = { "t1 : "int", "t2" : "t3 -> str"}
			     sub2 = { "t3" : "str", "t4" : "t2 -> t1"}
					 Applying substitutions:
					 self = { "t1" : "int", "t2" : "str -> str"}
			     sub2 = { "t3" : "str", "t4" : "(t3 -> str) -> int"}
					 Union:
			     { "t1" : "int", "t2" : "str -> str", "t3" : "str", "t4" : "t3 -> str -> int" }

					 TODO What about deeper subsitutions? (e.g. t3 above in t4's sig)
		"""
		for each_type in self.subs.values():
			each_type.apply_subst(sub2)
		self.subs = self.subs.update(sub2.subs)
		return self
