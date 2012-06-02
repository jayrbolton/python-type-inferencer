class Substitution:
	"""
	A substitution is a mapping of type labels to types
		e.g. { "t1" : "t0{}",
					 "t2" : "t4{a:t5, b:int}}
	subs is a dictionary that holds this mapping.
	"""
	def __init__(self, subs=None):
		if subs == None: self.subs = {}
		else: self.subs = subs
	
	def __repr__(self):
		s = "["
		for (key,val) in self.subs.iteritems():
			s += str(key) + " >> " + str(val) + ","
		s += "]"
		return s

	def merge(self,other_sub): self.subs.update(other_sub.subs)

	def add(self,label,typ): self.subs[label] = typ

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
			each_type.apply_sub(sub2)
		self.subs = self.subs.update(sub2.subs)
		return self
