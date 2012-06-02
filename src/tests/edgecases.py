
"""
Global Hell
"""

x = 99

print(x)

def soup():
	global x
	x = 1
	def fasdlkf():
		x = 7
		print(x)
		global x
		x = 33
	fasdlkf()
	print(x)
	return x

soup()

print(x)
