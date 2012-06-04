from typed_ast import *
from tnode import *
from .. import substitution as subst
from ..types import typ
from tname import *
from tlist import *
from ttuple import *
from tattribute import *

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
		if not self.typ: self.typ = typ.TError("Untyped value in assignment")

		(target_node, tsub, tenv) = typed_ast.TypedAST.traverse(self.node.targets[0], env)
		target_node.typ = self.typ
		self.targets = [target_node]
		if isinstance(target_node, TName):
			env.add_type(self.typ, target_node.id)
			sub = subst.Substitution({target_node.id : self.typ})
		elif isinstance(target_node, TAttribute):
			self_given = env.get_type('self')
			if self_given:
				self_given.attributes.add_type(self.typ, target_node.attr)
			else:
				self_type = typ.TSelf({target_node.attr : self.typ})
				env.add_type(self_type, 'self')
			sub = subst.Substitution({target_node.attr : self.typ})
		logging.debug("Envenvenv: " + str(env))
		# elif isinstance(target_node, TList):
		# elif isinstance(target_node, TTuple):
		return (self, sub, env)
