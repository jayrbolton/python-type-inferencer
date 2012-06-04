
from typed_ast import *
from tnode import *
from .. import substitution as sub
from ..types import typ

class TList(TNode):
	"""
	A node representing a list of values.
	"""

	def __init__(self, n):
		super(TList,self).__init__(n)
		self.name = "List"
		self.elts = []

	def format_tree(self,indents):
		s = super(TList,self).format_tree(indents)
		s += "  "*indents + "Elements: \n"
		for e in self.elts: s += e.format_tree(indents+1)
		return s

	def traverse(self, env):
		logging.info("Traversing a list...")
		self.typ = typ.TList([])
		for e in self.node.elts:
			(elem_node, elem_sub, elem_env) = typed_ast.TypedAST.traverse(e, env)
			self.elts.append(elem_node)
			self.typ.contained.append(elem_node.typ)
		return (self, elem_sub, env)
