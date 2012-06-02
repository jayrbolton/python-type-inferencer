from typed_ast import *
from tnode import *
from .. import substitution as sub
from .. import typ

class TModule(TNode):
	"""
	A module token with type information.
	"""

	def __init__(self,n,filename,src):
		self.node = node
		self.name = filename
		self.source = src
		self.body = []
		self.typ  = typ.TObj({})

	def traverse(self, n, env):
		logging.info("Traversing a module...")
		for n in node.body:
			(node1,sub1,env1) = TypedAST.traverse(n, env)
			env.merge(env1)
			self.body.append(node1)
			self.typ.add_attr(node1.typ, node1.name)
		return (self, sub.Substitution(), env)

	def format_tree(self, indents):
		s = super(TModule,self).format_tree(indents)
		s += "  "*indents + "Body: \n"
		for n in self.body: s += n.format_tree(indents+1)
		return s
