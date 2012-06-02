
class TFunctionDef(TNode):
	"""
	A function definition node.
	"""

	def __init__(self, n):
		super(TCall,self).__init__(n)
		self.name = "Function Definition"

	def format_tree(self, indents):
		s = super(TFunctionDef,self).format_tree(indents)
		s += "  "*indents + "Name: " + self.fname + "\n"
		s += "  "*indents + "Arguments:\n" + self.args.format_tree(indents+1)
		s += "  "*indents + "Body: \n"
		for n in self.body: s+= n.format_tree(indents+1)
		return s

	def traverse(self, env):
		# Create a new environment with the parameters removed from the parent
		# environment (for shadowing) and create a tuple of parameter types
		self.args = TArgs(self.node.args)
		self.fname = self.node.name
		param_names,param_types = [],[]
		for arg in self.arg.args:
			param_names.append(arg.id)
			param_types.append(typ.TObj({}))
		env_scoped = copy.deepcopy(env)
		for name in env.attrs.iterkeys():
			if name == "self": pass
			elif name in arg_names: del env_scoped.attrs[name]
		self.args.typ = typ.TTuple(param_types)

		# Traverse the body with the scoped environment.
		self.body = []
		for n in node.body:
			(node1,sub1,env1) = TypedAST.traverse(n, env_scoped)
			self.body.append(node1)
			env_scoped.merge(env1)
			self.args.typ.apply_sub(sub1)

		# Construct all the parameter and return types and encompass them in the function type.
		return_type = env_scoped.get_type("return")
		if return_type == None: return_type = typ.TBuiltin(type(None))
		func_type = typ.TObj({"*params" : self.args.typ, "*return" : return_type})

		# Add the function name and type to the parent environment
		env.add_type(func_type, self.node.name)
		return (self, sub1, env)
