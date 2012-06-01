"""
A data structure that encompasses information about python programs.

So far, it is simply AST nodes mapped to type information.

TODO
type inference of multiple assignment (unpacking), and we could detect errors

"""

import sys, logging, types, builtins, re, copy, pdb

from typ import *
from ast import *

"""
Log all logging.info('wat') messages to logs/program_graph.log
"""
logging.basicConfig(filename='logs/program_graph.log',level=logging.DEBUG)

class ProgramGraph:
	"""
	An Abstract Syntax Tree with type annotations.
	"""

	def __init__(self,source):
		logging.info("Using the parsing module to parse 'source'...")
		self.parse_file(source)
		logging.info("Traversing our AST...")
		self.modules = []
		logging.info("Builtins: " + str(builtins.env))
		self.traverse(self.ast, builtins.env)
		logging.info("Analyzed Tree:")
		logging.info(self.format_tree())

	def __str__(self):
		return "program graph: " + ''.join([str(n) for n in self.modules])

	def parse_file(self,source):
		"""
		You can give this func a string of source code, a file object, or a
		string file name.
		"""
		m = "Cannot read from the provided file: " # for error handling below
		if isinstance(source, file):
			try:
				self.source = source.read()
				self.filename = source.name
			except: print(m); logging.error(m + source.name); raise
		elif isinstance(source, str):
			if(re.compile('.*\.py\Z').match(source)):
				# XXX we probably need more comprehensive filename parsing.
				try:
					self.filename = source
					self.source = open(source).read()
				except: print(m); logging.error(m + source); raise
			else:
				self.source = source
				self.filename = "Unknown"
		logging.info("Successfully loaded source (" + self.filename + "):\n" + self.source)
		self.ast = parse(self.source)
		logging.info("Parsed source. Raw AST is:\n" + dump(self.ast))

	def format_tree(self):
		"""
		Return a formatted string representing the tree.
		"""
		s = ""
		for t in self.modules:
			s += t.format_tree(1)
		return s

	def dump_ast(self):
		"""
		Print out the AST as a block of text showing AST objects and fields.
		"""
		print(dump(self.ast))

	def traverse(self, n, env):
		"""
		1. Descend the AST, converting all the AST nodes into our own Node objects.
		2. Infer the type of the current node.
		3. Return a pair of Substitution and Node.

		XXX: this could be done more OO-ish by using the NodeVisitor object.

		Returns a tuple of the Node, a Substitution, and an Environment.
		"""
		IS = isinstance
		if   IS(n, Module):        return self.infer_module(n, env)
		elif IS(n, Expr):          return self.infer_expr(n, env)
		elif IS(n, Num):           return self.infer_num(n, env)
		elif IS(n, Return):        return self.infer_return(n, env)
##	elif IS(n, Lambda):        return self.infer_lambda(n, env)
		elif IS(n, Assign):        return self.infer_assign(n, env)
		elif IS(n, FunctionDef):   return self.infer_funcdef(n, env)
		elif IS(n, Call):          return self.infer_call(n, env)
		elif IS(n, Str):           return self.infer_str(n, env)
		elif IS(n, Name):          return self.infer_name(n, env)
##	elif IS(n, List):          return self.infer_list(n, env)
##	elif IS(n, Dict):          return self.infer_dict(n, env)
		elif IS(n, ClassDef):      return self.infer_classdef(n,env)
		elif type(n).__name__ == "Attribute":     return self.infer_attribute(n,env)
		else:                     return (Node(n), Substitution(), env)

	def infer_module(self, node, env):
		ns = []
		for n in node.body:
			(node1,sub1,env1) = self.traverse(n, env)
			env.merge(env1)
			ns.append(node1)
		module = Node(node, self.filename,ns)
		self.modules.append(module)
		return (module, Substitution(), env)

	def infer_call(self, node, env):
		(node1, sub1, env1) = self.traverse(node.func, env)
		given_type = node1.info.get("typ")
		if isinstance(given_type,TError): # Bail out on an error
			return (Node(node, node1.name, typ=given_type),Substitution(),env)

		(arg_types,arg_names) = ([],[])
		if type(node.func).__name__ == "Attribute": # Automatically pass in self
			arg_names.append("self")
			arg_types.append(env.get_type("self"))
		for arg in node.args:
			(node2, sub2, env2) = self.traverse(arg, env)
			type2 = node2.info.get("typ")
			arg_types.append(type2)
			arg_names.append(node2.name)
		arg_tuple = TTuple(arg_types)
		rtype = given_type.attributes.get_type("*return")
		if rtype == None: rtype = TObj({})
		applied_type = TObj({"*params" : arg_tuple, "*return" : rtype})

		# Unify and substitute
		logging.debug("Given type: " + str(given_type))
		logging.debug("Applied type: " + str(applied_type))
		sub = applied_type.unify(given_type)
		logging.debug("Substitution: " + str(sub))
		applied_type.apply_sub(sub)
		unified_type = applied_type
		logging.debug("Unified type: " + str(unified_type))

		# Handle type error results from unification.
		if isinstance(unified_type,TError):
			return_type = unified_type
		else:
			return_type = unified_type.attributes.get_type("*return")
		# If there was a type error in the parameters, propogate it up
		err = unified_type.attributes.get_type("*params")
		if isinstance(err,TError):
			return_type = err

		n = Node(node, node1.name, typ=return_type)
		return (n, sub, env)

	def infer_assign(self, node, env):
		(value, sub1, env1) = self.traverse(node.value, env)
		env.merge(env1)
		value_type = value.info.get("typ")
		if not value_type: raise "RHS of assignment did not get a type."
		targets = []
		t = node.targets[0]
		targets.append(Node(t, t.id, typ=value_type))
		env.add_type(value_type, t.id)
		n = Node(node, "Assign", targets + [value], io="Program stack")
		return (n, Substitution({t.id : value_type}), env)

	def infer_funcdef(self, node, env):
			# Create a new environment with the parameters removed from the parent environment (shadowing)
			arg_names = [arg.id for arg in node.args.args]
			env_scoped = copy.deepcopy(env)
			for name in env.attrs.iterkeys():
				if name == "self": pass
				elif name in arg_names: del env_scoped.attrs[name]

			# Traverse the parameters.
			(param_nodes,param_types,param_names) = ([],[],[])
			for param in node.args.args:
				if not param.id == "self": env_scoped.add_type(TObj({}), param.id)
				(node1,sub1,env1) = self.traverse(param, env_scoped)
				param_nodes.append(node1)
				param_names.append(node1.name)
				param_type = node1.info.get("typ")
				param_types.append(node1.info.get("typ"))
			param_type = TTuple(param_types)

			# Traverse the body with the scoped environment.
			body = []
			for n in node.body:
				(node1,sub1,env1) = self.traverse(n, env_scoped)
				env_scoped.merge(env1)
				env_scoped.apply_sub(sub1)
				param_type.apply_sub(sub1)
				for n in param_nodes: n.info["typ"] = n.info.get("typ").apply_sub(sub1)
				body.append(node1)

			# Construct all the parameter and return types and encompass them in the function type.
			return_type = env_scoped.get_type("return")
			if return_type == None: return_type = TError("No return type")
			func_type = TObj({"*params" : param_type, "*return" : return_type})

			# Return the func node along with the old environment and the new substitution.
			env.add_type(func_type, node.name)
			param_node = Node(node.args, "Parameters", param_nodes, typ=param_type)
			func = Node(node, node.name, [param_node] + body, typ=func_type)
			logging.debug("env: " + str(env))
			logging.debug("env_scoped: " + str(env_scoped))
			return (func, sub1, env) ## XXX what sub to return?

##def infer_lambda(self, node, env):
##	arg_names = [arg.id for arg in node.args.args]
##	env_scoped = copy.deepcopy(env)
##	for name in env.types:
##		if name in arg_names: del env_scoped.types[name]

##	(args,arg_types) = ([],[])
##	for arg in node.args.args:
##		(node1,sub1,env1) = self.traverse(arg, env_scoped)
##		args.append(node1)
##		arg_type = node1.info.get("typ")
##		env_scoped.bind(node1.name, arg_type)
##		arg_types.append(node1.info.get("typ"))
##	args_node = Node(node.args, "", args)

##	(node1,sub1,env1) = self.traverse(node.body, env_scoped)
##	env_scoped.merge(env1)

##	return_type = env_scoped.types.get("return")
##	if not return_type: return_type = builtins.none_typ
##	arg_types.reverse() ## XXX inefficient
##	param_type = Builtin("tuple",tuple,arg_types)
##	func_type  = Arrow(param_type, return_type)

##	func = Node(node, "lambda", [args_node] + [node1], typ=Arrow(param_type,return_type))
##	return (func, sub1, env) ## XXX what sub to return?

	def infer_expr(self, node, env):
		(node1, sub1, env1) = self.traverse(node.value,env)
		n = Node(node,"",[node1])
		return (n, sub1, env1)

	def infer_return(self, node, env):
		(node1, sub1, env1) = self.traverse(node.value, env)
		env.apply_sub(sub1)
		env.add_type(node1.info.get("typ"), "return")
		n = Node(node, "return", [node1])
		return (n, sub1, env)

	def infer_num(self, node, env):
		typ = node.n.__class__
		n = Node(node, node.n, typ=TBuiltin(type(node.n)))
		return (n, Substitution(), env)

	def infer_str(self, node, env):
		n = Node(node,"\"" + node.s + "\"",typ=TBuiltin(type(node.s)))
		return (n, Substitution(), env)

	def infer_name(self, node, env):
		if node.id == "self":
			logging.debug("FOUND SELF")
			logging.debug("env : " + str(env))
			logging.debug("in env: " + str(env.get_type(node.id)))
			logging.debug(isinstance(env.get_type(node.id),TSelf))
		t = env.get_type(node.id)
		if t == None:
			t = TError("Undefined")
			env.add_type(t, node.id)
		n = Node(node, node.id, typ=t)
		return (n, Substitution(), env)

	def infer_classdef(self, node, env):
		"""
		Infer a class definition.  This will create a new type inserted into the
		environment, mapped to the name of the class.  The class's type holds a
		*return attribute that returns the object type.
		"""
		# Get the type of the superclass so we can merge into it.
		# for b in node.bases...

		# We need a new, scoped environment, but we don't have to worry about
		# shadowing.
		env_scoped = copy.deepcopy(env)
		# Loop over the body, adding attributes to our type as we go.
		(class_attrs, inst_attrs, ns) = ({}, {}, [])
		for n in node.body:
			(node1,sub1,env1) = self.traverse(n, env_scoped)
			if isinstance(n, Assign):
				typ = node1.children[0].info.get("typ")
				name = n.targets[0].id
				class_attrs[name] = typ
				inst_attrs[name] = typ
			if isinstance(n, FunctionDef):
				typ = node1.info.get("typ")
				name = node1.name
				first_param = typ.attributes.attrs.get("*params")
				if first_param: first_param = first_param.contained[0]
				if isinstance(first_param, TSelf):
					inst_attrs[name] = typ
				else: class_attrs[name] = typ
			env_scoped.merge(env1)
			ns.append(node1)

		# Construct the types based on our inferred list of attributes
		instance_type = TObj(inst_attrs)
		class_attrs.update({"*return":instance_type, "*params":TTuple([])})
		class_type = TObj(class_attrs,node.name)
		env.add_type(class_type, node.name)
		n = Node(node, node.name, ns, typ=class_type)
		return (n, Substitution(), env)

	def infer_attribute(self, node, env):
		"""
		Infer an attribute reference on an object; given a value (the object), and
		an attribute, perform a lookup in the type of the value for the attribute
		and return the type.
		"""
		(val_node,sub1,env1) = self.traverse(node.value,env)
		obj_type = val_node.info.get("typ")
		err = TError("Object: " + val_node.name + " has no attribute: " + node.attr)
		if obj_type == None: t = err
		else: t = obj_type.attributes.get_type(node.attr)
		if t == None: t = err
		n = Node(node, "Attribute", typ=t)
		return (n,Substitution(),env)

##def infer_list(self, node, env):
##	# TODO traverse the children of the list and put them in the applied Builtin type
##	n = Node(node, str(node.elts),typ=Builtin("list",type([])))
##	return (n,Substitution(), env)

##def infer_dict(self, node, env):
##	# TODO traverse the children of the dict and put them in the applied Builtin type
##	n = Node(node, str(node.keys),typ=Builtin("dict",type({})))
##	return (n,Substitution(), env)

class Node(ProgramGraph):
	def __init__(self, ast_node, name="", children=[], **info):
		self.ast_node = ast_node
		self.name = str(name)
		self.children = children
		self.info = info

	def __str__(self):
		s = self.name
		if "typ" in self.info:
			s += " : " + str(self.info["typ"])
		if "typ_err" in self.info: s += " <<Type error: " + str(self.info["typ_err"]) + ">>"
		return s + '\n'

	def format_tree(self,indents):
		s = "  " * indents + str(self)
		for c in self.children:
			s += c.format_tree(indents+1)
		return s
