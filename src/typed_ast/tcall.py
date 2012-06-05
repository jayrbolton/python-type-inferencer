from typed_ast import *
from tnode import *
from .. import substitution as subst
from ..types import typ
from tattribute import *

class TCall(TNode):
	"""
	A function call node.
	"""

	def __init__(self, n):
		super(TCall,self).__init__(n)
		self.name = "Function Call"
		self.args = []

	def format_tree(self, indents):
		s = super(TCall,self).format_tree(indents)
		s += "  "*indents + "Function: \n" + self.func.format_tree(indents+1)
		s += "  "*indents + "Arguments: \n"
		for a in self.args: s += a.format_tree(indents+1)
		return s

	def collect_errors(self): return super(TCall,self).collect_errors()

	def traverse(self, env):
		logging.info("Unifying a function call...")
		# From the function name, get the given type from the environment
		(node1, sub1, env1) = typed_ast.TypedAST.traverse(self.node.func, env)
		self.func = node1
		given_type = self.func.typ
		logging.info("Given type: " + str(given_type))
		if isinstance(given_type, typ.TError): # Bail out on an error
			self.typ = given_type
			self.typ.lineno = self.node.lineno
			return (self, subst.Substitution(), env)

		# Infer and construct the tuple of arguments
		# Then construct the applied type
		(arg_types, arg_names) = ([], [])
		first_param = given_type.get_attr("*return")
		if isinstance(first_param,typ.TSelf):
			arg_names.append("self")
			arg_types.append(typ.TSelf())
		for arg in self.node.args:
			(arg_node, arg_sub, arg_env) = typed_ast.TypedAST.traverse(arg, env)
			self.args.append(arg_node)
			arg_types.append(arg_node.typ)
			arg_names.append(arg_node.name)
		arg_tuple = typ.TTuple(arg_types)
		return_type = given_type.attributes.get_type("*return")
		if return_type == None: return_type = typ.TObj({})
		applied_type = typ.TObj({"*params" : arg_tuple, "*return" : return_type})
		logging.info("Applied type: " + str(applied_type))

		# Unify and substitute
		sub = applied_type.unify(given_type)
		logging.info("Substitution: " + str(sub))
		applied_type.apply_sub(sub)
		unified_type = applied_type
		logging.debug("Unified type: " + str(unified_type))

		# Handle type error results from unification.
		# If there was a type error in the parameters, propogate it up to the
		# return type
		# XXX this error type propagation is getting really ugly and unwieldy and crappy
		err = unified_type.attributes.get_type("*params")
		if isinstance(err,typ.TError):
			self.typ = err
			self.typ.lineno = self.node.lineno
		# Else if the unified type itself is an error, return that error
		elif isinstance(unified_type,typ.TError):
			self.typ = unified_type
			self.typ.lineno = self.node.lineno
		# 'err' itself is not an error, but we may have errors within the tuple
		elif isinstance(err, typ.TTuple):
			self.typ = unified_type.attributes.get_type("*return")
			for t in err.contained:
				if isinstance(t,typ.TError):
					self.typ = t
					self.typ.lineno = self.node.lineno

		return (self, sub, env)
