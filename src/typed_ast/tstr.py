
from typed_ast import *
from tnode import *
from .. import substitution as sub
from ..types import typ

class TStr(TNode):
	"""
	A node representing variable assignment
	"""

	def __init__(self, n):
		super(TStr,self).__init__(n)
		self.name = "String"

	def format_tree(self,indents):
		s = super(TStr,self).format_tree(indents)
		s += "  "*indents + "s =  " + self.s + "\n"
		return s

	def traverse(self, env):
		self.s = self.node.s
		self.typ = typ.TBuiltin(type(self.s))
		return (self, sub.Substitution(), env)

