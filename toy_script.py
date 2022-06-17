import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import pickle
import functions as f
import progressbar
# def find_rain(r, rain_rate):
#     k = 0.124
#     alpha = 1.061
#     rain_att = k * rain_rate ** alpha
#     return rain_att * (r / 1000)  # attenuation is in db/km
#
#
# distances = np.arange(1, 400, 1)
# fig, ax = plt.subplots()
# plt.plot(distances, [find_rain(r, 2.5) for r in distances], label='2.5')
# plt.plot(distances, [find_rain(r, 25) for r in distances], label='25')
# plt.plot(distances, [find_rain(r, 150) for r in distances], label='150')
# plt.legend()
# plt.show()
users = [900]
k = 1

def find_closest(user):
    x = np.minimum((x_bs - user[0]) % xDelta, (user[0] - x_bs) % xDelta)
    y = np.minimum((y_bs - user[1]) % yDelta, (user[1] - y_bs) % yDelta)
    return np.argsort(x ** 2 + y ** 2)[:k]

misalignments = []
for number_of_users in users:
    iteration_min, iteration_max = 0, 1000 #iterations[number_of_users]

    bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[
        progressbar.Bar('=', f'Scenario: {scenario}, #users: {number_of_users} [', ']'), ' ',
        progressbar.Percentage(), ' ', progressbar.ETA()])
    bar.start()

    for iteration in range(iteration_min, iteration_max):
        bar.update(iteration)
        opt_x = np.zeros((number_of_users, number_of_bs))
        np.random.seed(iteration)
        x_user, y_user = f.find_coordinates(number_of_users, Clustered)

        occupied_beams = np.zeros((number_of_bs, len(directions_bs)))

        for u in range(number_of_users):
            user_coords = f.user_coords(u, x_user, y_user)
            bs = list(find_closest(user_coords))
            number_of_links = 0
            bs = bs[0]
            bs_coords = f.bs_coords(bs)
            geo = f.find_geo(bs_coords, user_coords)
            beam_number = f.find_beam_number(geo, beamwidth_b)
            if occupied_beams[bs, beam_number] < users_per_beam:
                misalignments.append(f.find_misalignment(bs_coords, user_coords, beamwidth_b))

fig, ax = plt.subplots()
plt.hist(misalignments, density = True, bins = 20)
plt.xlim([-5, 5])
plt.show()