import numpy as np
import scipy.sparse as sp
import math
import matplotlib.pyplot as plt
import networkx as nx
import sys
from itertools import product
import initialization
import new_optimization
import os
from parameters import *
import functions as f

def utility_function(alpha, x):
    if alpha == 1:
        return np.log(x)
    else:
        return np.divide(np.power(x, (1-alpha)), (1-alpha))

fig, ax = plt.subplots()
x = np.arange(0, 5, 0.1)

print(x)
for alpha in [0, 1, 2]:
    plt.plot(x, utility_function(alpha, x), label = f"$\\alpha = {alpha}$")

plt.ylabel('$u_{\\alpha}(x)$')
plt.xlabel('$x$')
plt.legend()
plt.show()