"""
This is currently unused.

Schemes represent quantified type signatures.
"""

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
		self.new_sub = None

	def apply_sub(self, sub):
		"""
		Apply a Substitution dictionary to this scheme.
		In the case of Schemes, we introduce a new scope/context so we have to
		create a new Substitution which is the parent Substitution minus any new
		bound type variables. This can be compared to variable shadowing in a new
		scope.
		For example, if the type variable 'a' is in the global Substitution
		dictionary, but then we have the scheme 'Forall a. a -> b -> c', then the
		'Forall a' is not the same as the global 'a', so we need to remove that
		from the context.
		"""
		self.new_sub = sub
		for v in self.variables:
			if v in self.new_sub.subs: del self.new_sub.subs[v]
		self.typ = self.typ.apply_sub(self.new_sub)

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
		return self.typ.apply_sub(sub)
