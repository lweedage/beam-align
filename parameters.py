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

iterations = {50: 1, 100: 5000, 300: 1667, 500: 1000, 750: 667, 1000: 500}
# iterations = {50: 1, 100: 1250, 300: 417, 500: 250, 750: 167, 1000: 125}
# iterations = {50: 1, 100: 2, 300: 100, 500: 100, 750: 100, 1000: 100}

if beamwidth_b == math.radians(5):
    if users_per_beam == 1:
        misalignment = {100: 2.474298615223395, 300: 1.7711557465008643, 500: 1.4360941838490278, 750: 1.2665564292114155, 1000: 1.2032622331465102}
        user_misalignment = {100: 2.3179265606309314, 300: 1.762168662950395, 500: 1.535596309140072, 750: 1.3797275107000668, 1000: 1.2875087508096044}
    elif users_per_beam == 2:
        misalignment = {100: 2.3064171289945516, 300: 1.7429837600388332, 500: 1.5200853769797917, 750: 1.3704760825852744, 1000: 1.2795399384855486}
        user_misalignment = {100: 2.3179265606309314, 300: 1.762168662950395, 500: 1.535596309140072,
                         750: 1.3797275107000668, 1000: 1.2875087508096044}
    elif users_per_beam == 5:
        misalignment = {100: 2.304155378731202, 300: 1.7443041940911854, 500: 1.517791702678711, 750: 1.363242543889057, 1000: 1.2646044244259174}
    elif users_per_beam == 10:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}

elif beamwidth_b == math.radians(10):
    if users_per_beam == 1:
        misalignment =  {100: 4.776645670840895, 300: 3.1139353789452566, 500: 3.2944083553481947, 750: 2.4269086690163593, 1000: 2.2655298056446806}
    elif users_per_beam == 2:
        misalignment = {100: 4.554114054199489, 300: 3.45640873302682, 500: 3.052559491791455, 750: 2.8232608584700487, 1000: 2.811857156136495}
        user_misalignment = {100: 2.2803757183164755, 300: 1.8100531018666917, 500: 1.6241093282243912, 750: 1.5233427625330365, 1000: 1.511377808852402}
    elif users_per_beam == 5:
        misalignment = {100: 4.5488144780297155, 300: 3.4512171217874776, 500: 3.0203904557373344, 750: 2.712767200096782, 1000: 2.5342743753744146}
    elif users_per_beam == 10:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}

elif beamwidth_b == math.radians(15):
    if users_per_beam == 1:
        misalignment = {100: 6.799991533612523, 300: 5.417942708002498, 500: 5.379963384851986, 750: 5.2762251776046405, 1000: 5.0202205971746325}
    elif users_per_beam == 2:
        misalignment = {100: 6.8658298901623, 300: 5.631725472865619, 500: 5.2612506747458925, 750: 5.427178251242687, 1000: 6.222774008468761}
        user_misalignment = {100: 2.068225656851897, 300: 1.7011561232885326, 500: 1.591864526477323, 750: 1.5553193996200205, 1000: 1.631569478937228}
    elif users_per_beam == 5:
        misalignment = {100: 6.856108651293654, 300: 5.594951393374119, 500: 5.088147995058014, 750: 4.744310518646445, 1000: 4.601993056211772}
    elif users_per_beam == 10:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}

RateRequirement = True
user_rate = 1000 # mbps

Torus = True