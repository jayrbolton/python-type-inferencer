"""
A data structure that encompasses information about python programs.

So far, it is simply AST nodes mapped to type information.

created: 1.22.12
updated: 2.10.12

todo:
	* clean up the giant traverse switch. you can probably break up all that shit
	  into functions. also, there is redundant code in there (eg, Lambda and
	  FuncDef)

"""

import sys, logging, types, builtins, re, copy

from inftype import *
from ast import *

"""
Log all logging.info('wat') messages to logs/pytown.log
"""
logging.basicConfig(filename='logs/pytown.log',level=logging.DEBUG)

class ProgramGraph:

	def __init__(self,source):
		logging.info("Using the parsing module to parse 'source'...")
		self.parse_file(source)
		logging.info("Traversing our AST...")
		self.modules = []
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
				# XXX we probably need more comprehensive filename parsing. (-jay)
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

	def traverse(self, node, env):
		## TODO: make an inference module that mixes into this class. Simplify this
		## case statement into function calls to the many type inference functions.
		"""
		1. Descend the AST, converting all the AST node into our own Node objects.
		2. Infer the type of the current node.
		3. Return a pair of Substitution and Node.

		Returns a tuple of the Node, a Substitution, and an Environment.
		"""
		if isinstance(node, Module):
			ns = []
			for n in node.body:
				(node1,sub1,env1) = self.traverse(n, env)
				env.apply_subst(sub1)
				env.merge(env1)
				ns.append(node1)
			module = Node(node,self.filename,ns)
			self.modules.append(module)
			return (module, Substitution(), env)
		elif isinstance(node, Expr):
			(node1, sub1, env1) = self.traverse(node.value,env)
			n = Node(node,"",[node1])
			return (n, Substitution(), env1)
		elif isinstance(node, Num):
			typ = node.n.__class__
			n = Node(node,node.n,typ=Instance(typ.__name__,typ))
			return (n, Substitution(), env)
		elif isinstance(node, Return):
			(node1, sub1, env1) = self.traverse(node.value,env)
			env.bind("return", node1.info.get("typ"))
			n = Node(node,"return",[node1])
			return (n, Substitution(), env)
		elif isinstance(node, Lambda):
			arg_names = [arg.id for arg in node.args.args] # 1.
			env_scoped = copy.deepcopy(env)
			for name in env.types:
				if name in arg_names: del env_scoped.types[name]

			(args,arg_types) = ([],[])
			for arg in node.args.args:
				(node1,sub1,env1) = self.traverse(arg, env_scoped)
				args.append(node1)
				arg_type = node1.info.get("typ")
				env_scoped.bind(node1.name, arg_type)
				arg_types.append(node1.info.get("typ"))
			args_node = Node(node.args, "", args)

			(node1,sub1,env1) = self.traverse(node.body, env_scoped)
			env_scoped.apply_subst(sub1)
			env_scoped.merge(env1)

			return_type = env_scoped.types.get("return")
			if not return_type: return_type = builtins.none_typ
			arg_types.reverse() ## XXX inefficient
			param_type = Instance("tuple",tuple,arg_types)
			func_type  = Arrow(param_type, return_type)

			func = Node(node, "lambda", [args_node] + [node1], typ=Arrow(param_type,return_type))
			return (func, sub1, env) ## XXX what sub to return?

		elif isinstance(node, Assign):
			(value, sub1, env1) = self.traverse(node.value, env)
			env.apply_subst(sub1)
			env.merge(env1)
			value_type = value.info.get("typ")
			if not value_type: raise "RHS of assignment did not get a type."
			targets = []
			for t in node.targets:
				targets.append(Node(t, t.id, typ=value_type))
				env.bind(t.id, value_type)
			n = Node(node, "", targets + [value], io="Program stack")
			return (n, sub1, env)
		elif isinstance(node, FunctionDef):
			"""
			1. Create a new environment with the parameters removed from the parent environment (shadowing)
			2. Traverse the body with the scoped environment.
			3. Now traverse the parameters with the new type information returned from traversing the body.
			4. Return the func node along with the old environment and the new substitution.
			"""
			arg_names = [arg.id for arg in node.args.args] # 1.
			env_scoped = copy.deepcopy(env)
			for name in env.types:
				if name in arg_names: del env_scoped.types[name]

			(args,arg_types) = ([],[])
			for arg in node.args.args:
				(node1,sub1,env1) = self.traverse(arg, env_scoped)
				args.append(node1)
				arg_type = node1.info.get("typ")
				env_scoped.bind(node1.name, arg_type)
				arg_types.append(node1.info.get("typ"))
			args_node = Node(node.args, "", args)

			body = []
			for n in node.body:
				(node1,sub1,env1) = self.traverse(n, env_scoped)
				env_scoped.apply_subst(sub1)
				env_scoped.merge(env1)
				body.append(node1)

			return_type = env_scoped.types.get("return")
			if not return_type: return_type = builtins.none_typ
			arg_types.reverse() ## XXX inefficient
			param_type = Instance("tuple",tuple,arg_types)
			func_type = Arrow(param_type, return_type)

			env.bind(node.name, func_type)
			func = Node(node, node.name, [args_node] + body, typ=Arrow(param_type,return_type))
			return (func, sub1, env) ## XXX what sub to return?
		elif isinstance(node, Call):
			(node1, sub1, env1) = self.traverse(node.func, env)
			type1 = node1.info.get("typ")

			arg_types = []
			for arg in node.args:
				(node2, sub2, env2) = self.traverse(node.args[0], env)
				type2 = node2.info.get("typ")
				arg_types.append(type2)
			arg_type = Instance("tuple",tuple,arg_types)

			logging.debug("arg_type: " + str(arg_type))
			applied_type = Arrow(arg_type, Variable())
			logging.debug("applied_type @149: " + str(applied_type))
			logging.debug("type1 @150: " + str(type1))
			sub3 = applied_type.unify(type1)
			logging.debug("unified sub: " + str(sub3))
			logging.debug("type1: " + str(type1))
			unified_type = type1.apply_subst(sub3)
			logging.debug("unified type: " + str(unified_type))

			n = Node(node, node1.name, typ=unified_type)
			return (n,Substitution(), env)
		elif isinstance(node, Str):
			n = Node(node,"\"" + node.s + "\"",typ=Instance(type(node.s).__name__,type(node.s)))
			return (n, Substitution(), env)
		elif isinstance(node, Name):
			n = Node(node, node.id)
			type_in_env = env.types.get(node.id)
			if type_in_env: n.info["typ"] = type_in_env
			else: n.info["typ"] = Variable() #n.info["typ_err"] = str(node.id) + " undefined"
			return (n, Substitution(), env)
		elif isinstance(node,List):
			# TODO traverse the children of the list and put them in the applied Instance type
			n = Node(node,str(node.elts),typ=Instance("list",type([])))
			return (n,Substitution(), env)
		elif isinstance(node,Dict):
			# TODO traverse the children of the dict and put them in the applied Instance type
			n = Node(node,str(node.keys),typ=Instance("dict",type({})))
			return (n,Substitution(), env)
		else:
			return (Node(node), Substitution(), env)


class Node(ProgramGraph):
	def __init__(self, ast_node, name="", children=[], **info):
		self.ast_node = ast_node
		self.name = str(name)
		self.children = children
		self.info = info

	def __str__(self):
		s = self.name
		if "typ" in self.info: s += " : " + str(self.info["typ"])
		if "typ_err" in self.info: s += " <<Type error: " + str(self.info["typ_err"]) + ">>"
		return s + '\n'

	def __repr__(self):
		s = self.name
		if self.info["typ"]: s += " : " + str(self.info["typ"])
		return s

	def format_tree(self,indents):
		s = ""
		s += "  " * indents
		s += str(self)
		for c in self.children:
			s += c.format_tree(indents+1)
		return s
