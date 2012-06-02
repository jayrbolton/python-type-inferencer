import sys
from src.typed_ast.typed_ast import *

def main(argv):
	env = TypedAST(argv[0])

def usage():
	print("Usage:")
	print("jython main.py <source>")
	print("  where <source> is a file or directory of python source code that you want to infer")

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		usage()
		sys.exit()
	main(sys.argv[1:])
