from typed_ast import *
from tnode import *
from .. import substitution as sub
from ..types import typ
from tname import *

class TAssign(TNode):
	"""
	A node representing variable assignment
	"""

	def __init__(self, n):
		super(TAssign,self).__init__(n)
		self.name = "Assignment"

	def format_tree(self,indents):
		s = super(TAssign,self).format_tree(indents)
		s += "  "*indents + "Targets: \n"
		for t in self.targets: s += t.format_tree(indents+1)
		s += "  "*indents + "Value: \n" + self.value.format_tree(indents+1)
		return s

	def traverse(self, env):
		# Infer the type of the value
		(val_node, val_sub, val_env) = typed_ast.TypedAST.traverse(self.node.value, env)
		env.merge(val_env)
		self.value = val_node
		self.typ = self.value.typ
		if not self.typ: self.typ = typ.TError("Invalid value in assignment")

		# Infer targets. Multiple target assignment makes it way more complicated.
		self.targets = []
		for t in self.node.targets:
			self.targets.append(TName(t))
			self.targets[-1].id = t.id
		if len(self.targets) > 1: # We have multiple assignment
			iterable = getattr(self.typ,"contained",None)
			if not iterable:
				err = typ.TError("Multiple assignment to non-iterable value.")
				for t in self.targets: t.typ = err
			elif len(iterable) < len(self.targets):
				err = typ.TError("Too few values in multiple assignment")
				for t in self.targets: t.typ = err
			elif len(iterable) < len(self.targets):
				err = typ.TError("Too many values in multiple assignment")
				for t in self.targets: t.typ = err
			else:
				for tar,val in zip(self.targets,iterable): tar.typ = val.typ
		else: self.targets[0].typ = self.typ

		for t in self.targets: env.add_type(t.typ, t.id)
		return (self, sub.Substitution({t.id : self.typ}), env)

