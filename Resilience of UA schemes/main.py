from parameters import *
import matplotlib.pyplot as plt
import functions as f
import model as m
import association_schemes as a

x_user, y_user = f.find_coordinates(lambda_U)
number_of_users = len(x_user)

distances, gain_bs, gain_user, path_loss, SNR, SINR, nlos_probability = m.gain_SNR_pathloss(x_user, y_user)

k = 1
print(SNR, SINR)

links = a.strongest_SNR(number_of_users, SNR, k)
fig, ax = plt.subplots()
f.draw_graph(x_bs, y_bs, x_user, y_user, links, ax)
plt.title(f"SNR, k = {k}")
plt.show()

links = a.strongest_SINR(number_of_users, SINR, k)
fig, ax = plt.subplots()
f.draw_graph(x_bs, y_bs, x_user, y_user, links, ax)
plt.title(f"SINR, k = {k}")
plt.show()

links = a.closest(number_of_users, distances, SNR, k)
fig, ax = plt.subplots()
f.draw_graph(x_bs, y_bs, x_user, y_user, links, ax)
plt.title(f"Distance, k = {k}")
plt.show()

links = a.online_load(number_of_users, SNR)
fig, ax = plt.subplots()
f.draw_graph(x_bs, y_bs, x_user, y_user, links, ax)
plt.title(f"Load balancing, online")
plt.show()