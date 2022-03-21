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
import time

subdivisions = 2

class Segment():
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        self.links = dict()
        self.blockers = list()

    def split_x(self):
        new_segment1 = Segment(self.xmin, self.ymin, (self.xmin + self.xmax)/2, self.ymax)
        new_segment2 = Segment((self.xmin + self.xmax)/2, self.ymin, self.xmax, self.ymax)

        for [coord1, coord2], [user, bs] in self.links.items():
            coord1_new, bs_shift = find_modified_coords(coord1, coord2)
            if bs_shift != (0, 0):
                coord2_new = (coord2[0] + bs_shift[0], coord2[1] + bs_shift[1])
                coords = [(coord1, coord2_new), (coord1_new, coord2)]
            else:
                coords = [(coord1, coord2)]

            for coord1, coord2 in coords:
                left, right = False, False

                if coord1[0] <= (self.xmin + self.xmax)/2 or coord2[0] <= (self.xmin + self.xmax)/2:
                    left = True
                if coord1[0] > (self.xmin + self.xmax)/2 or coord2[0] > (self.xmin + self.xmax)/2:
                    right = True
                if left:
                    new_segment1.links[coord1, coord2] = [user, bs]
                if right:
                    new_segment2.links[coord1, coord2] = [user, bs]

        for blocker in self.blockers:
            first, last = blocker.boundary
            left, right = False, False

            if first.x <= (self.xmin + self.xmax)/2 or last.x <= (self.xmin + self.xmax)/2:
                left = True
            if first.x > (self.xmin + self.xmax)/2 or last.x > (self.xmin + self.xmax)/2:
                right = True

            if left:
                new_segment1.blockers.append(blocker)
            if right:
                new_segment2.blockers.append(blocker)
        return new_segment1, new_segment2

    def split_y(self):
        new_segment1 = Segment(self.xmin, self.ymin, self.xmax, (self.ymin + self.ymax) / 2)
        new_segment2 = Segment(self.xmin, (self.ymin + self.ymax) / 2, self.xmax, self.ymax)
        for [coord1, coord2], [user, bs] in self.links.items():
            coord1_new, bs_shift = find_modified_coords(coord1, coord2)
            if bs_shift != (0, 0):
                coord2_new = (coord2[0] + bs_shift[0], coord2[1] + bs_shift[1])
                coords = [(coord1, coord2_new), (coord1_new, coord2)]
            else:
                coords = [(coord1, coord2)]

            for coord1, coord2 in coords:
                left, right = False, False

                if coord1[1] <= (self.ymin + self.ymax) / 2 or coord2[1] <= (self.ymin + self.ymax) / 2:
                    left = True
                if coord1[1] > (self.ymin + self.ymax) / 2 or coord2[1] > (self.ymin + self.ymax) / 2:
                    right = True
                if left:
                    new_segment1.links[coord1, coord2] = [user, bs]
                if right:
                    new_segment2.links[coord1, coord2] = [user, bs]

        for blocker in self.blockers:
            first, last = blocker.boundary
            left, right = False, False

            if first.y <= (self.ymin + self.ymax) / 2 or last.y <= (self.ymin + self.ymax) / 2:
                left = True
            if first.y > (self.ymin + self.ymax) / 2 or last.y > (self.ymin + self.ymax) / 2:
                right = True

            if left:
                new_segment1.blockers.append(blocker)
            if right:
                new_segment2.blockers.append(blocker)

        return new_segment1, new_segment2

    def split(self):
        sega, segb = self.split_x()
        seg1, seg2 = sega.split_y()
        seg3, seg4 = segb.split_y()
        return seg1, seg2, seg3, seg4

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
    segment = Segment(xmin, ymin, xmax, ymax)

    while area < max_area:
        x_c, y_c = np.random.uniform(0, xmax), np.random.uniform(0, ymax)
        width, length = np.random.uniform(1, 25), np.random.uniform(1, 25)
        angle = np.random.uniform(0, 2 * math.pi)
        rectangle = Rectangle(x_c, y_c, angle, length, width)
        for blocker in rectangle.line_segments:
            segment.blockers.append(blocker)
        area += rectangle.area

    return segment


def draw_blockers(rectangles, ax):
    for i in range(2 ** (subdivisions * 2)):
        for rectangle in rectangles[i]:
            p = matplotlib.patches.Polygon(rectangle.coords)
            ax.add_patch(p)


def find_modified_coords(coord_1, coord_2):
    (x_1, y_1) = coord_1
    bs_shift_x, bs_shift_y = 0, 0

    if (max(coord_2[0], coord_1[0]) - min(coord_2[0], coord_1[0])) > (
            min(coord_2[0], coord_1[0]) - max(coord_2[0], coord_1[0])) % xDelta:
        if coord_2[0] > coord_1[0]:
            x_1 = coord_1[0] + xDelta
            bs_shift_x = -xDelta
        else:
            x_1 = coord_1[0] - xDelta
            bs_shift_x = xDelta

    if (max(coord_2[1], coord_1[1]) - min(coord_2[1], coord_1[1])) > (
            min(coord_2[1], coord_1[1]) - max(coord_2[1], coord_1[1])) % yDelta:
        if coord_2[1] > coord_1[1]:
            y_1 = coord_1[1] + yDelta
            bs_shift_y = -yDelta
        else:
            y_1 = coord_1[1] - yDelta
            bs_shift_y = yDelta

    return (x_1, y_1), [bs_shift_x, bs_shift_y]


def is_connection_blocked(user, bs, blockers):

    user = find_modified_coords(user, bs)
    s = LineString([user, bs])
    intersect = s.intersects(blockers)
    return intersect

def plot_blockers(blockers, ax):
    patchPoly = PolygonPatch(blockers)
    ax.add_patch(patchPoly)

def find_blocked_connections(opt_x, x_user, y_user, number_of_users):
    blockers = segmentation(opt_x, x_user, y_user, number_of_users)
    connection_blocked = np.zeros((number_of_users, number_of_bs))
    for blocker in blockers:
        for (coord1, coord2), (user, bs) in blocker.links.items():
            s = LineString([coord1, coord2])
            lines = blocker.blockers
            for line in lines:
                if s.intersects(line):
                    connection_blocked[user, bs] = 1
    return connection_blocked

def segmentation(opt_x, x_user, y_user, number_of_users):
    segment = simulate_blockers()

    for i in range(number_of_users):
        for j in range(number_of_bs):
            if opt_x[i, j] > 0:
                segment.links[(x_user[i], y_user[i]), (x_bs[j], y_bs[j])] = (i,j)

    to_split = [segment]
    finished = []

    while to_split:
        seg = to_split.pop(0)
        segments = seg.split()
        for segment in segments:
            if len(segment.links.values()) > 200:
                to_split.append(segment)
            else:
                finished.append(segment)

    return finished

if __name__ == '__main__':
    x_user, y_user = f.find_coordinates(100)
    number_of_users = len(x_user)

    name = str(
        'users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(
            users_per_beam))
    optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))

    opt_x = optimal[0]


    print(find_blocked_connections(opt_x, x_user, y_user, number_of_users))
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

