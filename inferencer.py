"""
Inferencer module. 

Created: 2.8.12 (J Bolton)
"""


def inf_module(node):
		ns = []
		for n in node.body:
			(node1,sub1,env1) = self.traverse(n, env)
			env.apply_subst(sub1)
			env.merge(env1)
			ns.append(node1)
		module = Node(node,self.file_name,ns)
		self.modules.append(module)
		return (module, Substitution(), env)


def inf_expr
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
			env_scoped = env
			for name in env_scoped.types:
				if name in arg_names: del env_scoped.types[name]

			body = []
			for n in node.body:
				(node1,sub1,env1) = self.traverse(n, env_scoped)
				env_scoped.apply_subst(sub1)
				env_scoped.merge(env1)
				body.append(node1)

			(args,arg_types) = ([],[])
			for arg in node.args.args:
				(node1,sub1,env1) = self.traverse(arg, env_scoped)
				args.append(node1)
				arg_types.append(node1.info.get("typ"))
			args_node = Node(node.args, "", args)

			return_type = env_scoped.types.get("return")
			if not return_type: return_type = Instance("none",type(None))
			param_type = Union(arg_types)
			func_type = Arrow(param_type, return_type)

			env.bind(node.name, func_type)
			func = Node(node, node.name, [args_node] + body, typ=Arrow(param_type,return_type))
			return (func, sub1, env) ## XXX what sub to return?
		elif isinstance(node, Call):
			"""
			ti env (EApp e1 e2) =
			    do tv       <- freshTVar "a"
			       (s1, t1) <- ti env e1
			       (s2, t2) <- ti (apply s1 env) e2
			       s3       <- mgu (apply s2 t1) (TArr t2 tv)
			       return (s3 `after` s2 `after` s1, apply s3 tv)
			"""
			tv = Variable()
			(node1, sub1, env1) = self.traverse(node.func, env)
			type1 = node1.info.get("typ")
			env.apply_subst(sub1)
			print("sub1 @136: " + str(sub1))
			print("env @136: " + str(env))

			arg_types = []
			for arg in node.args:
				(node2, sub2, env2) = self.traverse(node.args[0], env)
				type2 = node2.info.get("typ")
				arg_types.append(type2)
				type1.apply_subst(sub2)
			arg_type = Union(arg_types)
			print("arg_types @145: " + str(arg_types))
			print("arg_type @146: " + str(arg_type))

			applied_type = Arrow(arg_type, tv)
			print("applied_type @149: " + str(applied_type))
			print("type1 @150: " + str(type1))
			sub3 = applied_type.unify(type1)
			print("applied_type @152: " + str(applied_type))
			print("type1 @153: " + str(type1))
			print("sub3 @154: " + str(sub3))

			n = Node(node, node1.name, typ=type1)
			return (n, sub3, env)
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
