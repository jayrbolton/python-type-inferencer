
from typed_ast import *
from tnode import *
from .. import substitution as sub
from .. import typ

class TReturn(TNode):
	"""
	A node representing variable assignment
	"""

	def __init__(self, n):
		super(TReturn,self).__init__(n)
		self.name = "Returnment"

	def format_tree(self,indents):
		s = super(TReturn,self).format_tree(indents)
		s += "  "*indents + "Value: \n" + self.value.format_tree(indents+1)
		return s

	def traverse(self, env):
		(node1, sub1, env1) = TypedAST.traverse(node.value, env)
		self.value = node1
		self.typ = node1.typ
		env.add_type(self.typ, "return")
		return (self, sub1, env)

