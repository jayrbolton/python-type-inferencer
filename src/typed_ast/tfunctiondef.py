from typed_ast import *
from tnode import *
from .. import substitution as sub
from ..types import typ
from targs import *

class TFunctionDef(TNode):
	"""
	A function definition node.
	"""

	def __init__(self, n):
		super(TFunctionDef,self).__init__(n)
		self.name = "Function Definition"

	def format_tree(self, indents):
		s = super(TFunctionDef,self).format_tree(indents)
		s += "  "*indents + "Name: " + self.fname + "\n"
		s += "  "*indents + "Arguments:\n" + self.args.format_tree(indents+1)
		s += "  "*indents + "Body: \n"
		for n in self.body: s+= n.format_tree(indents+1)
		return s

	def collect_errors(self):
		es = super(TFunctionDef,self).collect_errors()
		for n in self.body: es += n.collect_errors()
		return es

	def traverse(self, env):
		# Create a new environment with the parameters removed from the parent
		# environment (for shadowing) and create a tuple of parameter types
		self.args = TArgs(self.node.args)
		self.fname = self.node.name
		param_names,param_types = [],[]
		for arg in self.args.args:
			param_names.append(arg)
			if arg != "self":
				t = typ.TObj({})
				t.open_type = True
				param_types.append(t)
			else: param_types.append(typ.TSelf())
		env_scoped = copy.deepcopy(env)
		for name,t in env.attrs.iteritems():
			if name in param_names: del env_scoped.attrs[name]
		for name,t in zip(param_names,param_types): env_scoped.add_type(t,name)
		self.args.typ = typ.TTuple(param_types)

		# Traverse the body with the scoped environment.
		self.body = []
		for n in self.node.body:
			(node1,sub1,env1) = typed_ast.TypedAST.traverse(n, env_scoped)
			self.body.append(node1)
			env_scoped.merge(env1)
			env_scoped.apply_sub(sub1)
			self.args.typ.apply_sub(sub1)

		# Construct all the parameter and return types and encompass them in the function type.
		return_type = env_scoped.get_type("return")
		if return_type == None: return_type = typ.TBuiltin(type(None))
		func_type = typ.TObj({"*params" : self.args.typ, "*return" : return_type})
		self.typ = func_type

		# Percolate the self type up to the parent environment
		self_type = env_scoped.get_type('self')
		if self_type: env.add_type(self_type,'self')

		# Add the function name and type to the parent environment
		env.add_type(func_type, self.node.name)
		return (self, sub1, env)
