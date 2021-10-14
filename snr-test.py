import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum
import numpy as np
import scipy.sparse as sp
import math
import matplotlib.pyplot as plt
import networkx as nx
import sys
from itertools import product

name = 'Simulations/simulation_' + str(19) + 'seed' + str(5)

iteration = 9999

objective_fixedSNR19 = np.loadtxt(name + 'objectives' + 'log' + 'snr1' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedSNR_fixed19 = np.loadtxt(name + 'objectives' + 'log' + 'snr2' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedclosest19 = np.loadtxt(name + 'objectives' + 'log' + 'snr3' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedoptimal19 = np.loadtxt(name + 'objectives' + 'log' + 'snr4' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixed1c19 = np.loadtxt(name + 'objectives' + 'log' + 'snr5' + 'fixed_BW' + str(iteration) + '.txt')

objective_fairSNR19 = np.loadtxt(name + 'objectives' + 'log' + 'snr1' + 'fair_BW' + str(iteration) + '.txt')
objective_fairSNR_fixed19 = np.loadtxt(name + 'objectives' + 'log' + 'snr2' + 'fair_BW' + str(iteration) + '.txt')
objective_fairclosest19 = np.loadtxt(name + 'objectives' + 'log' + 'snr3' + 'fair_BW' + str(iteration) + '.txt')
objective_fairoptimal19 = np.loadtxt(name + 'objectives' + 'log' + 'snr4' + 'fair_BW' + str(iteration) + '.txt')
objective_fair1c19 = np.loadtxt(name + 'objectives' + 'log' + 'snr5' + 'fair_BW' + str(iteration) + '.txt')

name = 'Simulations/simulation_' + str(19) + 'seed' + str(5)

iteration = 9999

objective_fixedSNR22 = np.loadtxt(name + 'objectives' + 'log' + 'snr1' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedSNR_fixed22 = np.loadtxt(name + 'objectives' + 'log' + 'snr2' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedclosest22 = np.loadtxt(name + 'objectives' + 'log' + 'snr3' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedoptimal22 = np.loadtxt(name + 'objectives' + 'log' + 'snr4' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixed1c22 = np.loadtxt(name + 'objectives' + 'log' + 'snr5' + 'fixed_BW' + str(iteration) + '.txt')

objective_fairSNR22 = np.loadtxt(name + 'objectives' + 'log' + 'snr1' + 'fair_BW' + str(iteration) + '.txt')
objective_fairSNR_fixed22 = np.loadtxt(name + 'objectives' + 'log' + 'snr2' + 'fair_BW' + str(iteration) + '.txt')
objective_fairclosest22 = np.loadtxt(name + 'objectives' + 'log' + 'snr3' + 'fair_BW' + str(iteration) + '.txt')
objective_fairoptimal22 = np.loadtxt(name + 'objectives' + 'log' + 'snr4' + 'fair_BW' + str(iteration) + '.txt')
objective_fair1c22 = np.loadtxt(name + 'objectives' + 'log' + 'snr5' + 'fair_BW' + str(iteration) + '.txt')

def average(x):
    return sum(x)/len(x)

data19_fixedBW = [objective_fixedSNR19, objective_fixedclosest19, objective_fixedSNR_fixed19, objective_fixedoptimal19, objective_fixed1c19]
data19_fairBW = [objective_fairSNR19, objective_fairclosest19, objective_fairSNR_fixed19, objective_fairoptimal19, objective_fair1c19]

data22_fixedBW = [objective_fixedSNR22, objective_fixedclosest22, objective_fixedSNR_fixed22, objective_fixedoptimal22, objective_fixed1c22]
data22_fairBW = [objective_fairSNR22, objective_fairclosest22, objective_fairSNR_fixed22, objective_fairoptimal22, objective_fair1c22]


print('Fixed BW - simulation 19:', [average(data19_fixedBW[i]) for i in range(5)])
print('Fair BW - simulation 19:', [average(data19_fairBW[i]) for i in range(5)])
print('Fixed BW - simulation 22:', [average(data22_fixedBW[i]) for i in range(5)])
print('Fair BW - simulation 22:', [average(data22_fairBW[i]) for i in range(5)])



fig, ax = plt.subplots()
plt.boxplot(data19_fixedBW)
plt.title('Fixed BW - 19')
# plt.xticks([1, 2, 3, 4, 5], ['SNR', 'closest', 'fixed SNR', 'optimal', '1 connection'])
plt.show()

fig, ax = plt.subplots()
plt.boxplot(data19_fairBW)
plt.title('Fair BW - 19')
# plt.xticks([1, 2, 3, 4, 5], ['SNR', 'closest', 'fixed SNR', 'optimal', '1 connection'])
plt.show()


fig, ax = plt.subplots()
plt.boxplot(data22_fixedBW)
# plt.xticks([1, 2, 3, 4, 5], ['SNR', 'closest', 'fixed SNR', 'optimal', '1 connection'])
plt.title('Fixed BW - 22')
plt.show()

fig, ax = plt.subplots()
plt.boxplot(data22_fairBW)
# plt.xticks([1, 2, 3, 4, 5], ['SNR', 'closest', 'fixed SNR', 'optimal', '1 connection'])
plt.title('Fair BW - 22')
plt.show()

