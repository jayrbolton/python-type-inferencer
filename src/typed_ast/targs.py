from typed_ast import *
from tnode import *
from .. import substitution as sub
from ..types import typ

class TArgs(TNode):

	def __init__(self,n):
		super(TArgs, self).__init__(n)
		self.name = "Arguments"
		self.args = [n.id for n in n.args]

	def format_tree(self,indents): return super(TArgs,self).format_tree(indents)
