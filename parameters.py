import math
from cycler import cycler
import matplotlib

matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed'])
colors =  ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100

def find_scenario(scenario):
    if scenario in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]:
        beamwidth_deg = 5
    elif scenario in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]:
        beamwidth_deg = 10
    else:
        beamwidth_deg = 15

    if scenario in [1, 2, 3, 4, 5, 6]:
        users_per_beam = 1
    elif scenario in [7, 8, 9, 10, 11, 12, 25, 26, 27, 28, 29, 30]:
        users_per_beam = 2
    elif scenario in [13, 14, 15, 16, 17, 18]:
        users_per_beam = 5
    elif scenario in [19, 20, 21, 22, 23, 24]:
        users_per_beam = 10
    else:
        users_per_beam = False

    if scenario in [1, 2, 3, 7, 8, 9, 13, 14, 15, 19, 20, 21, 25, 26, 27]:
        Penalty = True
    else:
        Penalty = False

    if scenario in [25, 26, 27, 28, 29, 30]:
        Clustered = True
    else:
        Clustered = False

    return beamwidth_deg, users_per_beam, Penalty, Clustered

scenario = int(input('Scenario?'))
# scenario = 1
beamwidth_deg, users_per_beam, Penalty, Clustered = find_scenario(scenario)

pi = math.pi
bs_of_interest = 10
radius = 50  # for triangular grid

xmin, xmax = 0, 200
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

beamwidth_u = math.radians(5)

beamwidth_b = math.radians(int(beamwidth_deg))

W = 200 # in MHz  # bandwidth

if Penalty:
    M = 100  # penalty on having disconnected users
else:
    M = 0

# users_per_beam = 2  # amount of users in a beam
# users_per_beam = int(input("Users per beam?"))

transmission_power = 10 ** 2.0  # 20 dB
noise_figure = 7.8
noise_power_db = -174 + 10 * math.log10(W * 10 ** 9) + noise_figure
noise = 10 ** (noise_power_db / 10)

BS_height = 10
user_height = 1.5
centre_frequency = 28e9
propagation_velocity = 3e8

SINR_min = 10 ** (5 / 10)

directions_bs = range(int(2 * pi / beamwidth_b))
directions_u = range(int(2 * pi / beamwidth_u))


def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j % 2) * radius < xmax and j * dy < ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs


x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)

# iterations = {50: 1, 100: 5000, 300: 1667, 500: 1000, 750: 667, 1000: 500}
iterations = {50: 1, 100: 1250, 300: 417, 500: 250, 750: 167, 1000: 125}
# iterations = {50: 1, 100: 2, 300: 100, 500: 100, 750: 100, 1000: 100}
# iterations = {50: 1, 100: 5000, 300: 1667, 500: 1000, 750: 5000, 1000: 500}

if beamwidth_b == math.radians(5):
    misalignment = {100: 2.305281309802043, 300: 1.8052022485970176, 500: 1.612339843868333, 750: 1.4901366392132527,
     1000: 1.422366940934934}

elif beamwidth_b == math.radians(10):
    misalignment = {100: 4.614016371773798, 300: 3.620447464260859, 500: 3.2624919090013247, 750: 3.044722901246334,
                    1000: 2.9192438129820375}

elif beamwidth_b == math.radians(15):
    misalignment = {100: 6.915414299578208, 300: 5.950506540997203, 500: 5.5587922187759, 750: 5.28075100142384,
                    1000: 5.0947598231896025}

RateRequirement = True
user_rate = 1000 # mbps

Torus = True
