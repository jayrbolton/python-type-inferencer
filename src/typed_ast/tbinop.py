from typed_ast import *
from tnode import *
from tcall import *
from .. import substitution as subst
from ..types import typ

class TBinOp(TNode):
	"""
	A node representing an expression.
	"""

	def __init__(self, n):
		super(TBinOp,self).__init__(n)
		self.name = "Binary Operator"

	def format_tree(self,indents):
		s = super(TBinOp,self).format_tree(indents)
		s += "  "*indents + "Operator: " + self.op + "\n"
		s += "  "*indents + "Left: \n" + self.left.format_tree(indents+1)
		s += "  "*indents + "Right: \n" + self.right.format_tree(indents+1)
		return s

	def collect_errors(self):
		es = super(TBinOp,self).collect_errors()
		es += self.left.collect_errors()
		es += self.right.collect_errors()
		return es

	def traverse(self, env):
		self.op = "__" + type(self.node.op).__name__.lower() + "__"
		(left_node, lsub, lenv) = typed_ast.TypedAST.traverse(self.node.left,env)
		(right_node, rsub, renv) = typed_ast.TypedAST.traverse(self.node.right,env)
		self.left = left_node
		self.right = right_node
		op_type = left_node.typ.get_attr(self.op)
		if not op_type:
			self.typ = typ.TError("Operator: " + self.op + " undefined in " + str(left_node.typ.label),self.node.lineno)
		else: 
			applied_type = typ.TObj({"*return" : op_type.get_attr("*return"),
			                     "*params" : typ.TTuple([typ.TSelf(),right_node.typ])})
			print(op_type)
			print(applied_type)
			sub = applied_type.unify(op_type)
			print(sub)
			applied_type.apply_sub(sub)
			print(applied_type)
			self.typ = applied_type.get_attr("*return")
			if isinstance(applied_type.get_attr("*params"),typ.TError):
				self.typ = applied_type.get_attr("*params")
		return (self, lsub, env)
