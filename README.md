# Python Type Inference

* Much of it is finished, with a full model for structural type inference built out.
* Quickly run the demo with: $ jython demo.py
* Step through the demo by hitting <ENTER>
* See /paper/PythonTypeInference.pdf to read about the new type inference system I created for this project.
* See my slides for Evergreen's spring SOS project presentations: https://docs.google.com/presentation/d/19vKKkBxZPOV1TP4DecFaXtIoMewjXlAVXo2GhZ0t0j0/edit?pli=1#slide=id.p

# General Usage
 * $ jython infer.py <source_code.py>
 * eg: $ jython main.py tests/src/functions.py
 * The output will go in logs/pytown.log


The program's actual content is under /src/.

If you're interested in structural type inference (type inference of duck typing), please contact me at jayrbolton@gmail.com
