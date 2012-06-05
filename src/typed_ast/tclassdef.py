
from typed_ast import *
from tnode import *
from .. import substitution as sub
from ..types import typ

class TClassDef(TNode):
	"""
	A node representing variable assignment
	"""

	def __init__(self, n):
		super(TClassDef,self).__init__(n)
		self.name = "Class Definition"
		self.bases = []
		self.body = []

	def format_tree(self,indents):
		s = super(TClassDef,self).format_tree(indents)
		s += "  "*indents + "Name: " + self.cname + "\n"
		s += "  "*indents + "Superclasses: " + str(self.bases) + "\n"
		s += "  "*indents + "Body: \n"
		for n in self.body: s += n.format_tree(indents+1)
		return s

	def collect_errors(self):
		es = super(TClassDef,self).collect_errors()
		for n in self.body: es += n.collect_errors() 
		return es

	def traverse(self, env):
		"""
		Infer a class definition.  This will create a new type inserted into the
		environment, mapped to the name of the class.  The class's type holds a
		*return attribute that returns the object type.
		"""
		# Get the type of the superclass so we can merge into it.
		# for b in node.bases...

		# We need a new, scoped environment, but we don't have to worry about
		# shadowing.
		env_scoped = copy.deepcopy(env)
		self.cname = self.node.name
		# Loop over the body, adding attributes to our type as we go.
		class_attrs, inst_attrs = {}, {}
		for n in self.node.body:
			(node1,sub1,env1) = typed_ast.TypedAST.traverse(n, env_scoped)
			self.body.append(node1)
			env_scoped.merge(env1)
			if isinstance(n, Assign):
				for n in node1.targets:
					class_attrs[n.id] = node1.typ
					inst_attrs[n.id] = node1.typ
			if isinstance(n, FunctionDef):
				# Catch the constructor and get the attributes applied to 'self'
				params = node1.typ.get_attr("*params")
				if params:
					first_param = params.contained[0]
					if node1.fname == "__init__":
						if isinstance(first_param, typ.TSelf):
							self_type = env1.get_type('self')
							if self_type: inst_attrs.update(self_type.attributes.attrs)
						else:
							node1.typ = TError("First parameter of __init__ must be self")
					else:
						if isinstance(first_param, typ.TSelf):
							inst_attrs[node1.fname] = node1.typ
						else: class_attrs[node1.fname] = node1.typ

		# Construct the types based on our inferred list of attributes
		instance_type = typ.TObj(inst_attrs)
		class_attrs.update({"*return":instance_type, "*params":typ.TTuple([])})
		self.typ = typ.TObj(class_attrs,self.cname)
		env.add_type(self.typ, self.cname)
		return (self, sub.Substitution(), env)
