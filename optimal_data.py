import matplotlib.pyplot as plt
# from parameters import *
import numpy as np
import pickle
import seaborn as sns
import math

colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100
markers = ['o', 's' , 'v' , '*', 'p', 'P', '1', '+']

iterations = {120: 10, 300: 10, 601: 10, 902: 10, 1202: 10}

radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

users = [int(i / (xDelta / 1000 * yDelta / 1000)) for i in [100, 250, 500, 750, 1000]]

M = 10000
beamwidth_deg = 10
s = 1
user_rate = 500

Shares = False


if Shares:
    x1 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(1) + str(user_rate) +  '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(2) + str(user_rate) + '.p'), 'rb')).values()
    # x3 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(5) + str(user_rate) + '.p'), 'rb')).values()
    x4 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(10) + str(user_rate) + '.p'), 'rb')).values()
    x5 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(1000) + str(user_rate) + '.p'), 'rb')).values()

    plt.plot(users, x1, '--', marker=markers[0], label='$s=1$', color=colors[0])
    plt.plot(users, x2, '--', marker=markers[1], label='$s=2$', color=colors[1])
    # plt.plot(users, x3, '--', marker=markers[2], label='$s=5$', color=colors[2])
    plt.plot(users, x4, '--', marker=markers[3], label='$s=10$', color=colors[3])
    plt.plot(users, x5, '--', marker=markers[4], label='$s=\infty$', color=colors[4])

else:
    x1 = pickle.load(open(str('Data/Processed/cap' + str(5) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x3 = pickle.load(open(str('Data/Processed/cap' + str(15) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    plt.plot(users, x1, '--', marker=markers[0], label='$\\theta^b = 5\\degree$', color=colors[0])
    plt.plot(users, x2, '--', marker=markers[1], label='$\\theta^b = 10\\degree$', color=colors[1])
    plt.plot(users, x3, '--', marker=markers[2], label='$\\theta^b = 15\\degree$', color=colors[2])


plt.xlabel('Number of users')
plt.ylabel('Total capacity (Mbps)')
plt.legend()
plt.show()


if Shares:
    x1 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(1) + str(user_rate) + '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(2) + str(user_rate) + '.p'), 'rb')).values()
    # x3 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(5) + str(user_rate) + '.p'), 'rb')).values()
    x4 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(10) + str(user_rate) + '.p'), 'rb')).values()
    x5 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(1000) + str(user_rate) + '.p'), 'rb')).values()

    x1 = [sum(x) / len(x) for x in x1]
    x2 = [sum(x) / len(x) for x in x2]
    # x3 = [sum(x) / len(x) for x in x3]
    x4 = [sum(x) / len(x) for x in x4]
    x5 = [sum(x) / len(x) for x in x5]

    plt.plot(users, x1, '--', marker=markers[0], label='$s=1$', color=colors[0])
    plt.plot(users, x2, '--', marker=markers[1], label='$s=2$', color=colors[1])
    # plt.plot(users, x3, '--', marker=markers[2], label='$s=5$', color=colors[2])
    plt.plot(users, x4, '--', marker=markers[3], label='$s=10$', color=colors[3])
    plt.plot(users, x5, '--', marker=markers[4], label='$s=\infty$', color=colors[4])


else:
    x1 = pickle.load(open(str('Data/Processed/fair' + str(5) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/fair' + str(10) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x3 = pickle.load(open(str('Data/Processed/fair' + str(15) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

    x1 = [sum(x) / len(x) for x in x1]
    x2 = [sum(x) / len(x) for x in x2]
    x3 = [sum(x) / len(x) for x in x3]

    plt.plot(users, x1, '--', marker=markers[0], label='$\\theta^b = 5\\degree$', color=colors[0])
    plt.plot(users, x2, '--', marker=markers[1], label='$\\theta^b = 10\\degree$', color=colors[1])
    plt.plot(users, x3, '--', marker=markers[2], label='$\\theta^b = 15\\degree$', color=colors[2])

plt.xlabel('Number of users')
plt.ylabel('Jain\'s fairness index')
plt.legend()
plt.show()

if Shares:
    x1 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(1) + str(user_rate) +  '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(2) + str(user_rate) + '.p'), 'rb')).values()
    # x3 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(5) + str(user_rate) + '.p'), 'rb')).values()
    x4 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(10) + str(user_rate) + '.p'), 'rb')).values()
    x5 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(1000) + str(user_rate) + '.p'), 'rb')).values()

    plt.plot(users, x1, '--', marker=markers[0], label='$s=1$', color=colors[0])
    plt.plot(users, x2, '--', marker=markers[1], label='$s=2$', color=colors[1])
    # plt.plot(users, x3, '--', marker=markers[2], label='$s=5$', color=colors[2])
    plt.plot(users, x4, '--', marker=markers[3], label='$s=10$', color=colors[3])
    plt.plot(users, x5, '--', marker=markers[4], label='$s=\infty$', color=colors[4])


else:
    x1 = pickle.load(open(str('Data/Processed/sat' + str(5) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/sat' + str(10) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x3 = pickle.load(open(str('Data/Processed/sat' + str(15) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

    plt.plot(users, x1, '--', marker=markers[0], label='$\\theta^b = 5\\degree$', color=colors[0])
    plt.plot(users, x2, '--', marker=markers[1], label='$\\theta^b = 10\\degree$', color=colors[1])
    plt.plot(users, x3, '--', marker=markers[2], label='$\\theta^b = 15\\degree$', color=colors[2])

plt.xlabel('Number of users')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.show()

