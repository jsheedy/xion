#!/usr/bin/env python

from xion import Xion

xion = Xion(markov_matrix_size=100)
xion.train("HELLO FROM THE OTHER SIDE")
xion.normalize()

print(xion.speak())
