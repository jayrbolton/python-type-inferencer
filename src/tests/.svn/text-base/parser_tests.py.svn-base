
import unittest, sys
sys.path.append('../')
from inferencer.parser import *

class ParserTests(unittest.TestCase):

	def setUp(self):
		x = AST("tests/src/functions.py")

	def test_valid_construction(self):
		z = AST("tests/src/arithmetic.py")
	
	def test_invalid_construction(self):
		self.assertRaises(TypeError, AST)


if __name__ == "__main__":
	unittest.main()
