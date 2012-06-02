from typed_ast import *
from tnode import *
from .. import substitution as sub
from .. import typ

class TCall(TNode):
	"""
	A function call node.
	"""

	def __init__(self, n):
		super(TCall,self).__init__(n)
		self.name = "Function Call"

	def format_tree(self, indents):
		s = super(TCall,self).format_tree(indents)
		s += "  "*indents + "Function: \n" + self.func.format_tree(indents+1)
		s += "  "*indents + "Arguments: \n"
		for a in self.args: s += a.format_tree(indents+1)
		return s

	def traverse(self, env):
		logging.info("Unifying a function call...")
		# From the function name, get the given type from the environment 
		(node1, sub1, env1) = TypedAST.traverse(node.func, env)
		self.func = node1
		given_type = self.func.typ
		logging.info("Given type: " + str(given_type))
		if isinstance(given_type, typ.TError): # Bail out on an error
			return (self, sub.Substitution(), env)

		# Infer and construct the tuple of arguments
		# Then construct the applied type
		(arg_types, arg_names) = ([], [])
		if type(self.func).__name__ == "Attribute": # Automatically pass in self
			arg_names.append("self")
			arg_types.append(env.get_type("self"))
		for arg in node.args:
			(arg_node, arg_sub, arg_env) = self.traverse(arg, env)
			self.args.append(arg_node)
			arg_types.append(arg_node.typ)
			arg_names.append(arg_node.name)
		arg_tuple = typ.TTuple(arg_types)
		return_type = given_type.attributes.get_type("*return")
		if rtype == None: rtype = typ.TObj({})
		applied_type = typ.TObj({"*params" : arg_tuple, "*return" : rtype})
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
		err = unified_type.attributes.get_type("*params")
		if isinstance(err,typ.TError): return_type = err
		# Else if the unified type itself is an error, return that error
		elif isinstance(unified_type,typ.TError):
			return_type = unified_type
		# No error, so our return type is correct.
		else: return_type = unified_type.attributes.get_type("*return")

		return (self, sub, env)
