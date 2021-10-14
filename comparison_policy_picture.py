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

objective_fixedSNR19 = np.loadtxt(name + 'objectives' + 'log' + 'snr' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedSNR_fixed19 = np.loadtxt(name + 'objectives' + 'log' + 'snr_fixed10' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedclosest19 = np.loadtxt(name + 'objectives' + 'log' + 'closest' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedoptimal19 = np.loadtxt(name + 'objectives' + 'log' + 'optimal' + 'fixed_BW' + str(499) + '.txt')
objective_fixed1c19 = np.loadtxt(name + 'objectives' + 'log' + 'one_connection' + 'fixed_BW' + str(499) + '.txt')

objective_fairSNR19 = np.loadtxt(name + 'objectives' + 'log' + 'snr' + 'fair_BW' + str(iteration) + '.txt')
objective_fairSNR_fixed19 = np.loadtxt(name + 'objectives' + 'log' + 'snr_fixed10' + 'fair_BW' + str(iteration) + '.txt')
objective_fairclosest19 = np.loadtxt(name + 'objectives' + 'log' + 'closest' + 'fair_BW' + str(iteration) + '.txt')
objective_fairoptimal19 = np.loadtxt(name + 'objectives' + 'log' + 'optimal' + 'fair_BW' + str(499) + '.txt')
objective_fair1c19 = np.loadtxt(name + 'objectives' + 'log' + 'one_connection' + 'fair_BW' + str(499) + '.txt')

objective_optimalSNR19 = np.loadtxt(name + 'objectives' + 'log' + 'snr' + 'optimal_BW' + str(499) + '.txt')
objective_optimalSNR_fixed19 =  np.loadtxt(name + 'objectives' + 'log' + 'snr_fixed10' + 'optimal_BW' + str(499) + '.txt')
objective_optimalclosest19 = np.loadtxt(name + 'objectives' + 'log' + 'closest' + 'optimal_BW' + str(499) + '.txt')
objective_optimaloptimal19 = np.loadtxt(name + 'objectives' + 'log' + 'optimal' + 'optimal_BW' + str(499) + '.txt')
objective_optimal1c19 = np.loadtxt(name + 'objectives' + 'log' + 'one_connection' + 'optimal_BW' + str(499) + '.txt')

satisfaction_type1_fixedSNR19 = np.loadtxt(name + 'satisfaction_type1' + 'log' + 'snr' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type1_fixedclosest19 = np.loadtxt(name + 'satisfaction_type1' + 'log' + 'closest' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type1_fairSNR19 = np.loadtxt(name + 'satisfaction_type1' + 'log' + 'snr' + 'fair_BW' + str(iteration) + '.txt')
satisfaction_type1_fairclosest19 = np.loadtxt(name + 'satisfaction_type1' + 'log' + 'closest' + 'fair_BW' + str(iteration) + '.txt')

satisfaction_type2_fixedSNR19 = np.loadtxt(name + 'satisfaction_type2' + 'log' + 'snr' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type2_fixedclosest19 = np.loadtxt(name + 'satisfaction_type2' + 'log' + 'closest' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type2_fairSNR19 = np.loadtxt(name + 'satisfaction_type2' + 'log' + 'snr' + 'fair_BW' + str(iteration) + '.txt')
satisfaction_type2_fairclosest19 = np.loadtxt(name + 'satisfaction_type2' + 'log' + 'closest' + 'fair_BW' + str(iteration) + '.txt')

satisfaction_type3_fixedSNR19 = np.loadtxt(name + 'satisfaction_type3' + 'log' + 'snr' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type3_fixedclosest19 = np.loadtxt(name + 'satisfaction_type3' + 'log' + 'closest' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type3_fairSNR19 = np.loadtxt(name + 'satisfaction_type3' + 'log' + 'snr' + 'fair_BW' + str(iteration) + '.txt')
satisfaction_type3_fairclosest19 = np.loadtxt(name + 'satisfaction_type3' + 'log' + 'closest' + 'fair_BW' + str(iteration) + '.txt')

name = 'Simulations/simulation_' + str(22) + 'seed' + str(5)

iteration = 9999

objective_fixedSNR22 = np.loadtxt(name + 'objectives' + 'log' + 'snr' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedSNR_fixed22 = np.loadtxt(name + 'objectives' + 'log' + 'snr_fixed10' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedclosest22 = np.loadtxt(name + 'objectives' + 'log' + 'closest' + 'fixed_BW' + str(iteration) + '.txt')
objective_fixedoptimal22 = np.loadtxt(name + 'objectives' + 'log' + 'optimal' + 'fixed_BW' + str(499) + '.txt')
# objective_fixed1c22 = objective_fixedclosest22 #np.loadtxt(name + 'objectives' + 'log' + 'one_connection' + 'fixed_BW' + str(499) + '.txt')

objective_fairSNR22 = np.loadtxt(name + 'objectives' + 'log' + 'snr' + 'fair_BW' + str(iteration) + '.txt')
objective_fairSNR_fixed22 = np.loadtxt(name + 'objectives' + 'log' + 'snr_fixed10' + 'fair_BW' + str(iteration) + '.txt')
objective_fairclosest22 = np.loadtxt(name + 'objectives' + 'log' + 'closest' + 'fair_BW' + str(iteration) + '.txt')
objective_fairoptimal22 = np.loadtxt(name + 'objectives' + 'log' + 'optimal' + 'fair_BW' + str(499) + '.txt')
# objective_fair1c22 = np.loadtxt(name + 'objectives' + 'log' + 'one_connection' + 'fair_BW' + str(499) + '.txt')

objective_optimalSNR22 = np.loadtxt(name + 'objectives' + 'log' + 'snr' + 'optimal_BW' + str(499) + '.txt')
objective_optimalSNR_fixed22 = np.loadtxt(name + 'objectives' + 'log' + 'snr_fixed10' + 'optimal_BW' + str(499) + '.txt')
objective_optimalclosest22 = np.loadtxt(name + 'objectives' + 'log' + 'closest' + 'optimal_BW' + str(499) + '.txt')
objective_optimaloptimal22 = np.loadtxt(name + 'objectives' + 'log' + 'optimal' + 'optimal_BW' + str(499) + '.txt')
# objective_optimal1c22 = np.loadtxt(name + 'objectives' + 'log' + 'one_connection' + 'optimal_BW' + str(499) + '.txt')

satisfaction_type1_fixedSNR22 = np.loadtxt(name + 'satisfaction_type1' + 'log' + 'snr' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type1_fixedclosest22 = np.loadtxt(name + 'satisfaction_type1' + 'log' + 'closest' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type1_fairSNR22 = np.loadtxt(name + 'satisfaction_type1' + 'log' + 'snr' + 'fair_BW' + str(iteration) + '.txt')
satisfaction_type1_fairclosest22 = np.loadtxt(name + 'satisfaction_type1' + 'log' + 'closest' + 'fair_BW' + str(iteration) + '.txt')

satisfaction_type2_fixedSNR22 = np.loadtxt(name + 'satisfaction_type2' + 'log' + 'snr' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type2_fixedclosest22 = np.loadtxt(name + 'satisfaction_type2' + 'log' + 'closest' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type2_fairSNR22 = np.loadtxt(name + 'satisfaction_type2' + 'log' + 'snr' + 'fair_BW' + str(iteration) + '.txt')
satisfaction_type2_fairclosest22 = np.loadtxt(name + 'satisfaction_type2' + 'log' + 'closest' + 'fair_BW' + str(iteration) + '.txt')

satisfaction_type3_fixedSNR22 = np.loadtxt(name + 'satisfaction_type3' + 'log' + 'snr' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type3_fixedclosest22 = np.loadtxt(name + 'satisfaction_type3' + 'log' + 'closest' + 'fixed_BW' + str(iteration) + '.txt')
satisfaction_type3_fairSNR22 = np.loadtxt(name + 'satisfaction_type3' + 'log' + 'snr' + 'fair_BW' + str(iteration) + '.txt')
satisfaction_type3_fairclosest22 = np.loadtxt(name + 'satisfaction_type3' + 'log' + 'closest' + 'fair_BW' + str(iteration) + '.txt')

def average(x):
    return sum(x)/len(x)

satisfactionfairclosest19 = [satisfaction_type1_fairclosest19, satisfaction_type2_fairclosest19, satisfaction_type3_fairclosest19]
satisfactionfixedclosest19 = [satisfaction_type1_fixedclosest19, satisfaction_type2_fixedclosest19, satisfaction_type3_fixedclosest19]


satisfactionfairclosest22 = [satisfaction_type1_fairclosest22, satisfaction_type2_fairclosest22, satisfaction_type3_fairclosest22]
satisfactionfixedclosest22 = [satisfaction_type1_fixedclosest22, satisfaction_type2_fixedclosest22, satisfaction_type3_fixedclosest22]

data19_fixedBW = [objective_fixedSNR19, objective_fixedclosest19, objective_fixedSNR_fixed19, objective_fixedoptimal19, objective_fixed1c19]
data19_fairBW = [objective_fairSNR19, objective_fairclosest19, objective_fairSNR_fixed19, objective_fairoptimal19, objective_fair1c19]
data19_optimalBW = [objective_optimalSNR19, objective_optimalclosest19, objective_optimalSNR_fixed19, objective_optimaloptimal19, objective_optimal1c19]

data22_fixedBW = [objective_fixedSNR22, objective_fixedclosest22, objective_fixedSNR_fixed22, objective_fixedoptimal22]
data22_fairBW = [objective_fairSNR22, objective_fairclosest22, objective_fairSNR_fixed22, objective_fairoptimal22]
data22_optimalBW = [objective_optimalSNR22, objective_optimalclosest22, objective_optimalSNR_fixed22, objective_optimaloptimal22,]


print('Fixed BW - simulation 19:', [average(data19_fixedBW[i]) for i in range(5)])
print('Fair BW - simulation 19:', [average(data19_fairBW[i]) for i in range(5)])
print('Optimal BW - simulation 19:', [average(data19_optimalBW[i]) for i in range(5)])
print('Fixed BW - simulation 22:', [average(data22_fixedBW[i]) for i in range(4)])
print('Fair BW - simulation 22:', [average(data22_fairBW[i]) for i in range(4)])
print('Optimal BW - simulation 22:', [average(data22_optimalBW[i]) for i in range(4)])



fig, ax = plt.subplots()
plt.boxplot(data19_fixedBW)
plt.title('Fixed BW - 19')
plt.xticks([1, 2, 3, 4, 5], ['SNR', 'closest', 'fixed SNR', 'optimal', '1 connection'])
plt.show()

fig, ax = plt.subplots()
plt.boxplot(data19_fairBW)
plt.title('Fair BW - 19')
plt.xticks([1, 2, 3, 4, 5], ['SNR', 'closest', 'fixed SNR', 'optimal', '1 connection'])
plt.show()

fig, ax = plt.subplots()
plt.boxplot(data19_optimalBW)
plt.title('Optimal BW - 19')
plt.xticks([1, 2, 3, 4, 5], ['SNR', 'closest', 'fixed SNR', 'optimal', '1 connection'])
plt.show()


fig, ax = plt.subplots()
plt.boxplot(data22_fixedBW)
plt.xticks([1, 2, 3, 4], ['SNR', 'closest', 'fixed SNR', 'optimal'])
plt.title('Fixed BW - 22')
plt.show()

fig, ax = plt.subplots()
plt.boxplot(data22_fairBW)
plt.xticks([1, 2, 3, 4], ['SNR', 'closest', 'fixed SNR', 'optimal'])
plt.title('Fair BW - 22')
plt.show()

fig, ax = plt.subplots()
plt.boxplot(data22_optimalBW)
plt.xticks([1, 2, 3, 4], ['SNR', 'closest', 'fixed SNR', 'optimal'])
plt.title('Optimal BW - 22')
plt.show()

# fig, ax = plt.subplots()
# plt.boxplot(satisfactionfixedclosest19)
# plt.title('Satisfaction fixed closest 19')
# plt.show()
#
# fig, ax = plt.subplots()
# plt.boxplot(satisfactionfairclosest19)
# plt.title('Satisfaction fair closest 19')
# plt.show()
#
# fig, ax = plt.subplots()
# plt.boxplot(satisfactionfixedclosest22)
# plt.title('Satisfaction fixed closest 22')
# plt.show()
#
# fig, ax = plt.subplots()
# plt.boxplot(satisfactionfairclosest22)
# plt.title('Satisfaction fair closest 22')
# plt.show()