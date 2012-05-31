import ast

src = open("tests/src/demo.py").read()

demo = ast.parse(src)

class v(ast.NodeVisitor):
  def generic_visit(self,node,message):
    print(type(node).__name__)
    print(message)

  def visit_Module(self,node,msg):
    for b in node.body:
      self.visit(b,msg)

x = v()
# x.visit_Module(demo,"hi")

demo.inf_type = "hi"
