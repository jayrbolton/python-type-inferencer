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
