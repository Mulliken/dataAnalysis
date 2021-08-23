import subprocess as sub
import sys, json, copy
import itertools as it
import numpy as np


p = sub.Popen(['echo', 'text'], stdin=sub.PIPE, stdout=1)
inp = "text"
p.communicate(inp.encode())
print(f"Submitted")

