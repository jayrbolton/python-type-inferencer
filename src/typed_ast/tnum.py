
from tnode import *
from .. import substitution as sub
from ..types import typ

class TNum(TNode):
	"""
	A node representing variable assignment
	"""

	def __init__(self, n):
		super(TNum,self).__init__(n)
		self.name = "Number"

	def format_tree(self,indents):
		s = super(TNum,self).format_tree(indents)
		s += "  "*indents + "n =  " + str(self.n) + "\n"
		return s

	def traverse(self, env):
		self.n = self.node.n
		self.typ = typ.TBuiltin(type(self.n))
		return (self, sub.Substitution(), env)

