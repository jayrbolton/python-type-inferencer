"""
A data structure that encompasses information about python programs.
It is simply an AST tree with added type information tacked on.

TODO
type inference of multiple assignment (unpacking), and error detection for that.

"""

import sys, logging, types, re, copy, pdb

from .. import builtins
from .. import substitution as sub
from ..types import typ
from ast import *
from tnode import *

"""
Log all logging messages to logs/inference.log
"""
logging.basicConfig(filename='output/logs/inference.log',level=logging.DEBUG)

class TypedAST(object):
	"""
	A module token with type information.
	"""

	def __init__(self,source):
		logging.info("Parsing and traversing the source...")
		self.modules = [TypedAST.parse_file(source).traverse(builtins.env)]
		logging.info("Analyzed Tree:")
		logging.info(self.format_tree())

	def __str__(self): return "Typed AST: " + ''.join([str(n) for n in self.modules])

	@staticmethod
	def parse_file(source):
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
		logging.info("Loaded source (" + self.filename + "):\n" + self.source)
		mod = TModule(parse(self.source),filename,source)
		logging.info("Parsed source. Raw AST is:\n" + dump(mod.node,include_attributes=True))
		return mod

	def format_tree(self):
		"""
		Return a readable indented string representing the typed AST.
		"""
		s = ""
		for t in self.modules: s += t.format_tree(1)
		return s

	@staticmethod
	def traverse(n, env):
		"""
		Use some metaprogramming to get the class name of the node and call our own
		corresponding class.
		If we don't have a corresponding class, use the generic "TNode"

		-> Returns a type node
		"""
		clss = "T" + type(n).__name__
		subclasses = [c.__name__ for c in self.__subclasses__()]
		if clss in subclasses: clss = eval(clss)
		else: clss = TNode
		return clss(n).traverse(env)
