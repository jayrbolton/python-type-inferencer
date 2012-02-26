
import unittest, sys
sys.path.append('../')
from inferencer.inftype import *

class InftypeTests(unittest.TestCase):

	def setUp(self):
		self.var1 = Variable()
		self.var2 = Variable()
		self.var3 = Variable()
		self.int1 = Instance("int",int)
		self.float1 = Instance("float",float)
		self.str1 = Instance("str",str)
		self.arr1 = Arrow(self.int1,self.float1)
		self.arr2 = Arrow(self.var1,self.var2)
		self.arr3 = Arrow(self.var2,self.var3)
		self.arr4 = Arrow(self.str1,self.str1)
	
	def test_unification(self):
		## Unify two type vars
		# Different type vars unify
		self.assertEqual(self.var1.unify(self.var2).subs, {self.var1.name : self.var2})
		# Equal type vars do not unify
		self.assertEqual(self.var1.unify(self.var1).subs, {})

		## Unify type var with an instance (both directions)
		self.assertEqual(self.var1.unify(self.int1).subs, {self.var1.name : self.int1})
		self.assertEqual(self.str1.unify(self.var1).subs, {self.var1.name : self.str1})

		## Unify two instances (does not unify)
		self.assertEqual(self.int1.unify(self.str1).subs, {})

		## Unify a type var with an arrow (both directions)
		self.assertEqual(self.var1.unify(self.arr1).subs, {self.var1.name : self.arr1})
		self.assertEqual(self.arr1.unify(self.var1).subs, {self.var1.name : self.arr1})

		## Do each of the above but inside arrow types
		t0 = self.arr2.left.name
		t1 = self.arr2.right.name
		# Unify arrows of type vars of different names
		self.assertEqual(self.arr2.unify(self.arr3).subs, {t0 : self.arr3.left, t1 : self.arr3.right})
		# Unify arrows of type vars of same names (doesn't unify)
		self.assertEqual(self.arr1.unify(self.arr1).subs, {})
		# Unify an arrow of instances with one of type vars (both dirs)
		self.assertEqual(self.arr1.unify(self.arr2).subs, {t0 : self.arr1.left, t1 : self.arr1.right})
		self.assertEqual(self.arr2.unify(self.arr1).subs, {t0 : self.arr1.left, t1 : self.arr1.right})
		# Unify arrows of instances (does not unify)
		self.assertEqual(self.arr1.unify(self.arr4).subs, {})
		self.assertEqual(self.arr4.unify(self.arr1).subs, {})


if __name__ == "__main__":
	unittest.main()
