
import unittest, sys
sys.path.append('../')
from inferencer.pytown import *

class PytownTests(unittest.TestCase):

	def test_valid_construction(self):
		z = ProgramGraph("tests/src/arithmetic.py")
	
	def test_invalid_construction(self):
		self.assertRaises(TypeError, ProgramGraph)
	
	def test_constants_inf(self):
		p = ProgramGraph("tests/src/constants.py")
		## Not sure how to test this besides looking at logs...

	def test_function_def_inf(self):
		p = ProgramGraph("tests/src/functions.py")
		## Not sure how to test this besides looking at logs...


if __name__ == "__main__":
	unittest.main()
