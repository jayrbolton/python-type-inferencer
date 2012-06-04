
from typed_ast import *
from tnode import *
from .. import substitution as sub
from ..types import typ

class TAttribute(TNode):
	"""
	A node representing variable assignment
	"""

	def __init__(self, n):
		super(TAttribute,self).__init__(n)
		self.name = "Attribute Reference"

	def format_tree(self,indents):
		s = super(TAttribute,self).format_tree(indents)
		s += "  "*indents + "Object: \n" + self.value.format_tree(indents+1)
		s += "  "*indents + "Attribute: " + self.attr + "\n"
		return s

	def traverse(self, env):
		"""
		Infer an attribute reference on an object; given the object and an
		attribute, perform a lookup in the type of the object for the attribute and
		return that type.
		"""
		(val_node,val_sub,val_env) = typed_ast.TypedAST.traverse(self.node.value,env)
		self.value = val_node
		self.attr = self.node.attr
		err = typ.TError("Object: " + self.value.id + " has no attribute: " + self.attr)
		if self.value.typ == None: self.typ = err
		else: self.typ = self.value.typ.get_attr(self.node.attr)
		if self.typ == None: self.typ = err
		return (self, sub.Substitution(), env)
