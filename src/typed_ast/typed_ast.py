"""
A data structure that encompasses information about python programs.
It is simply an AST tree with added type information tacked on.

TODO
type inference of multiple assignment (unpacking), and error detection for that.

"""

import sys, logging, types, re, copy, pdb, os

from .. import builtins
from .. import substitution as sub
from .. import attributes as attr
from ..types import typ
from ast import *
from tmodule import *

mods = os.listdir('./src/typed_ast/')
mods = map(lambda x: x[:-3], filter(lambda x: x[-3:]==".py" and x!="__init__.py",mods))
for m in mods: exec("import " + m)

"""
Log all logging messages to logs/inference.log
"""
logging.basicConfig(filename='output/logs/inference.log',level=logging.DEBUG)

class TypedAST(object):
	"""
	A container and utility object that allows the parsing of python source code
	and the traversal of all our typed nodes.
	"""

	def __init__(self,source):
		logging.info("Parsing and traversing the source...")
		self.modules = []
		self.parse_file(source)
		self.modules[-1].traverse(attr.Attributes())
		logging.info("Analyzed Tree:")
		logging.info(self.format_tree())

	def __str__(self): return "Typed AST: " + ''.join([str(n) for n in self.modules])

	def parse_file(self,source):
		"""
		Open source code and return an abstract syntax tree using python's ast
		module.

		You can give this func a string of source code, a file object, or a
		string file name.
		-> Returns an ast.Module
		"""
		m = "Cannot read from the provided file: " # for error handling below
		if isinstance(source, file):
			try:
				logging.info("Source is a file object, reading")
				source = source.read()
				filename = source.name
			except: print(m); logging.error(m + source.name); raise
		elif isinstance(source, str):
			if(re.compile('.*\.py\Z').match(source)):
				try:
					logging.info("Source is a filename, opening and reading")
					filename = source
					source = open(source).read()
				except: print(m); logging.error(m + source); raise
			else:
				logging.info("Source is a string of source code")
				source = source
				filename = "Unknown"
		logging.info("Loaded source (" + filename + "):\n" + source)
		self.modules.append(TModule(parse(source),filename,source))
		logging.info("Parsed source. Raw AST is:\n" + dump(self.modules[-1].node,include_attributes=True))

	@staticmethod
	def pretty_dict(d, indent=0):
		for key, value in d.iteritems():
			print '  ' * indent + str(key)
			if isinstance(value, dict): pretty(value, indent+1)
			else: print '  ' * (indent+1) + str(value)

	def print_modules(self):
		for m in self.modules: TypedAST.pretty_dict(m.typ.attributes.attrs)

	def print_src(self):
		for m in self.modules: print(m.source)

	def format_tree(self):
		"""
		Return a readable indented string representing the typed AST.
		"""
		s = ""
		for m in self.modules: s += m.format_tree(1)
		return s

	def print_errors(self):
		es = self.collect_errors()
		print(str(len(es)) + " type errors.")
		for e in es: print(e)

	def collect_errors(self): 
		es = []
		for m in self.modules: es += m.collect_errors()
		return es

	@staticmethod
	def traverse(n, env):
		"""
		Use some metaprogramming to get the class name of the node and call our own
		corresponding class.
		If we don't have a corresponding class, use the generic "TNode"

		-> Returns a type node
		"""
		clss = "T" + type(n).__name__
		if clss.lower() in mods:
			mod = eval(clss.lower())
			clss = eval(clss.lower() + "." + clss)
		else:
			clss = tnode.TNode
		return clss(n).traverse(env)
