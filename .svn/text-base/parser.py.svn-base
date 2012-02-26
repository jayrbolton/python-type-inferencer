"""

A python parsing module that provides more functionality than the built-in "ast" module.

Created: 2.13.12 (j bolton)

"""

import ast, re, logging, sys, pprint

"""
Log all logging.info('wat') messages to logs/parser.log
"""
logging.basicConfig(filename='logs/parser.log',level=logging.DEBUG)

class AST:

	def __init__(self,source):
		"""
		You can give the constructor a string of source code, a file object, or a
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
		self.ast = ast.parse(self.source)
		logging.info("Parsed source. Raw AST is:\n" + ast.dump(self.ast))

	def __repr__(self):
		return ast.dump(self.ast)


def main():
	pass

if __name__ == "__main__":
	main()
