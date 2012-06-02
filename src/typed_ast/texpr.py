from typed_ast import *
from tnode import *
from .. import substitution as sub
from .. import typ

class TExpr(TNode):
	"""
	A node representing an expression.
	"""

	def __init__(self, n):
		super(TExpr,self).__init__(n)
		self.name = "Expression"

	def format_tree(self,indents):
		s = super(TAssign,self).format_tree(indents)
		s += "  "*indents + "Body: \n" + self.body.format_tree(indents+1)
		return s

	def traverse(self, env):
		(node1, sub1, env1) = TypedAST.traverse(self.node.value,env)
		self.body = node1
		self.typ = node1.typ
		return (self, sub1, env1)
