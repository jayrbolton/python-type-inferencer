from typed_ast import *
from tnode import *
from .. import substitution as sub
from .. import typ

class TArgs(TNode):
	
	def __init__(self,n):
		super(TArgs, self).__init_(n)
		self.name = "Arguments"
		self.args = [n.id for n in n.args]
	
	def format_tree(indents): return super(TArgs,self).format_tree(indents)
