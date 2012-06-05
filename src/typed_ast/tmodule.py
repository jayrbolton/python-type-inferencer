import typed_ast
from tnode import *
from .. import substitution as sub
from ..types import typ

class TModule(TNode):
	"""
	A module token with type information.
	"""

	def __init__(self,n,filename,src):
		super(TModule,self).__init__(n)
		self.name = filename
		self.source = src
		self.body = []
		self.typ = typ.TObj({},filename)

	def collect_errors(self):
		es = super(TModule,self).collect_errors()
		for n in self.body: es += n.collect_errors()
		return es

	def traverse(self, env):
		logging.info("Traversing a module...")
		for n in self.node.body:
			(node1,sub1,env1) = typed_ast.TypedAST.traverse(n, env)
			env.merge(env1)
			self.body.append(node1)
			self.typ.attributes.merge(env1)
		return (self, sub.Substitution(), env)

	def format_tree(self, indents):
		s = super(TModule,self).format_tree(indents)
		s += "  "*indents + "Body: \n"
		for n in self.body: s += n.format_tree(indents+1)
		return s
