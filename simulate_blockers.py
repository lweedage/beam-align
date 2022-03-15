import functions as f
from parameters import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches
from shapely.geometry import *
from shapely.ops import unary_union
from descartes import PolygonPatch
from shapely import affinity
import pickle

subdivisions = 2


class Rectangle():
    def __init__(self, x_c, y_c, angle, length, width):
        self.x_c = x_c
        self.y_c = y_c
        self.angle = angle
        self.length = length
        self.width = width

        gamma1 = np.arctan2(-width, length)
        self.x1 = x_c + math.cos(gamma1 + angle) * math.sqrt(width ** 2 + length ** 2) / 2
        self.y1 = y_c + math.sin(gamma1 + angle) * math.sqrt(width ** 2 + length ** 2) / 2

        gamma2 = np.arctan2(width, length)
        self.x2 = x_c + math.cos(gamma2 + angle) * math.sqrt(width ** 2 + length ** 2) / 2
        self.y2 = y_c + math.sin(gamma2 + angle) * math.sqrt(width ** 2 + length ** 2) / 2

        gamma3 = np.arctan2(width, -length)
        self.x3 = x_c + math.cos(gamma3 + angle) * math.sqrt(width ** 2 + length ** 2) / 2
        self.y3 = y_c + math.sin(gamma3 + angle) * math.sqrt(width ** 2 + length ** 2) / 2

        gamma4 = np.arctan2(-width, -length)
        self.x4 = x_c + math.cos(gamma4 + angle) * math.sqrt(width ** 2 + length ** 2) / 2
        self.y4 = y_c + math.sin(gamma4 + angle) * math.sqrt(width ** 2 + length ** 2) / 2

        self.coords = [(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3), (self.x4, self.y4)]
        self.points = (Point(self.x1, self.y1), Point(self.x2, self.y2), Point(self.x3, self.y3), Point(self.x4, self.y4))
        self.line_segments = [LineString([(self.x1, self.y1), (self.x2, self.y2)]),
                              LineString([(self.x1, self.y1), (self.x4, self.y4)]),
                              LineString([(self.x3, self.y3), (self.x4, self.y4)])]
        self.area = width * length

        self.poly = Polygon(self.points)


def simulate_blockers():
    max_area = 1 / 10 * xmax * ymax
    area = 0
    blockers = Polygon([])

    while blockers.area < max_area:
        x_c, y_c = np.random.uniform(0, xmax), np.random.uniform(0, ymax)
        width, length = np.random.uniform(1, 25), np.random.uniform(1, 25)
        angle = np.random.uniform(0, 2 * math.pi)
        rectangle = Rectangle(x_c, y_c, angle, length, width)

        blockers = unary_union([blockers, rectangle.poly])
    return blockers


def segmentation(x, y, index, x_center, y_center):
    if x <= x_center:
        x_center = x_center / 2
        if y >= y_center:
            index += '00'
            y_center = y_center + y_center / 2
        else:
            index += '01'
            y_center = y_center / 2
    elif x > x_center:
        x_center = x_center + x_center / 2
        if y >= y_center:
            index += '10'
            y_center = y_center + y_center / 2
        else:
            index += '11'
            y_center = y_center / 2
    return index, x_center, y_center


def find_which_part(coord):
    x, y = coord
    index = str()
    x_center, y_center = xmax / 2, ymax / 2
    for k in range(subdivisions):
        index, x_center, y_center = segmentation(x, y, index, x_center, y_center)
    return int(index, 2)


def draw_blockers(rectangles, ax):
    for i in range(2 ** (subdivisions * 2)):
        for rectangle in rectangles[i]:
            p = matplotlib.patches.Polygon(rectangle.coords)
            ax.add_patch(p)


def find_modified_coords(coord_1, coord_2):
    (x_1, y_1) = coord_1

    if (max(coord_2[0], coord_1[0]) - min(coord_2[0], coord_1[0])) > (
            min(coord_2[0], coord_1[0]) - max(coord_2[0], coord_1[0])) % xDelta:
        if coord_2[0] > coord_1[0]:
            x_1 = coord_1[0] + xDelta
        else:
            x_1 = coord_1[0] - xDelta

    if (max(coord_2[1], coord_1[1]) - min(coord_2[1], coord_1[1])) > (
            min(coord_2[1], coord_1[1]) - max(coord_2[1], coord_1[1])) % yDelta:
        if coord_2[1] > coord_1[1]:
            y_1 = coord_1[1] + yDelta
        else:
            y_1 = coord_1[1] - yDelta
    return (x_1, y_1)


def is_connection_blocked(user, bs, blockers):
    user = find_modified_coords(user, bs)
    s = LineString([user, bs])
    intersect = s.intersects(blockers)

    plt.plot([user[0], bs[0]], [user[1], bs[1]])

    return intersect

def plot_blockers(blockers, ax):
    patchPoly = PolygonPatch(blockers)
    ax.add_patch(patchPoly)

def blockers_on_torus():
    blockers = simulate_blockers()
    to_combine = [blockers]
    for shift in [(-xmax, ymax), (0, ymax), (xmax, ymax), (-xmax, 0), (xmax, 0), (-xmax, -ymax), (0, -ymax), (xmax, -ymax)]:
        new_blockers = affinity.translate(blockers, xoff = shift[0], yoff = shift[1])
        to_combine.append(new_blockers)
    torus_blockers = unary_union(to_combine)
    return torus_blockers

if __name__ == '__main__':
    for iteration in range(5000):
        print(iteration)
        np.random.seed(iteration)
        blockers = blockers_on_torus()
        pickle.dump(blockers, open(str('Data/Blockers/blockers' + str(iteration) + '.p'),'wb'), protocol=4)

    #
    # bs = (xmax - 100, 50)
    # x_user, y_user = f.find_coordinates(5)
    #
    # fig, ax = plt.subplots()
    #
    # for u in range(len(x_user)):
    #     user = (x_user[u], y_user[u])
    #     print(is_connection_blocked(user, bs, blockers))
    #
    # patchPoly = PolygonPatch(blockers,  fc='b', ec='b', alpha=1, zorder=2)
    # ax.add_patch(patchPoly)
    # plt.scatter(bs[0], bs[1])
    # plt.scatter(x_user, y_user)
    # plt.xlim([xmin - xmax, xmax + xmax])
    # plt.ylim([ymin - ymax, ymax + ymax])
    # plt.show()

