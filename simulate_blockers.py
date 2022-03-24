import pickle
import time

import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np
from descartes import PolygonPatch
from shapely.geometry import *

import functions as f
from parameters import *

subdivisions = 2


class Segment():
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        self.links = dict()
        self.blockers = list()

    @property
    def pair(self):
        return len(self.links) * len(self.blockers)

    @property
    def is_empty(self):
        return (len(self.links) == 0 or len(self.blockers) == 0)

    def split_x(self, mid_x=None):
        if mid_x == None:
            mid_x = (self.xmin + self.xmax) / 2
        new_segment1 = Segment(self.xmin, self.ymin, mid_x, self.ymax)
        new_segment2 = Segment(mid_x, self.ymin, self.xmax, self.ymax)

        for ((x1, y1), (x2, y2)), (user, bs) in self.links.items():
            if x2 < x1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            if x1 <= mid_x:
                if x2 <= mid_x:
                    new_segment1.links[(x1, y1), (x2, y2)] = (user, bs)
                else:
                    mid_y = y1 + (y2 - y1) * (mid_x - x1) / (x2 - x1)
                    new_segment1.links[(x1, y1), (mid_x, mid_y)] = (user, bs)
                    new_segment2.links[(mid_x, mid_y), (x2, y2)] = (user, bs)
            else:
                new_segment2.links[(x1, y1), (x2, y2)] = (user, bs)

        for (x1, y1), (x2, y2) in self.blockers:
            if x2 < x1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            if x1 <= mid_x:
                if x2 <= mid_x:
                    new_segment1.blockers.append(((x1, y1), (x2, y2)))
                else:
                    mid_y = y1 + (y2 - y1) * (mid_x - x1) / (x2 - x1)
                    new_segment1.blockers.append(((x1, y1), (mid_x, mid_y)))
                    new_segment2.blockers.append(((mid_x, mid_y), (x2, y2)))
            else:
                new_segment2.blockers.append(((x1, y1), (x2, y2)))

        return new_segment1, new_segment2

    def split_y(self, mid_y=None):
        if mid_y == None:
            mid_y = (self.ymin + self.ymax) / 2
        new_segment1 = Segment(self.xmin, self.ymin, self.xmax, mid_y)
        new_segment2 = Segment(self.xmin, mid_y, self.xmax, self.ymax)

        for ((x1, y1), (x2, y2)), (user, bs) in self.links.items():
            if y2 < y1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            if y1 <= mid_y:
                if y2 <= mid_y:
                    new_segment1.links[(x1, y1), (x2, y2)] = (user, bs)
                else:
                    mid_x = x1 + (x2 - x1) * (mid_y - y1) / (y2 - y1)
                    new_segment1.links[(x1, y1), (mid_x, mid_y)] = (user, bs)
                    new_segment2.links[(mid_x, mid_y), (x2, y2)] = (user, bs)
            else:
                new_segment2.links[(x1, y1), (x2, y2)] = (user, bs)

        for (x1, y1), (x2, y2) in self.blockers:
            if y2 < y1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            if y1 <= mid_y:
                if y2 <= mid_y:
                    new_segment1.blockers.append(((x1, y1), (x2, y2)))
                else:
                    mid_x = x1 + (x2 - x1) * (mid_y - y1) / (y2 - y1)
                    new_segment1.blockers.append(((x1, y1), (mid_x, mid_y)))
                    new_segment2.blockers.append(((mid_x, mid_y), (x2, y2)))
            else:
                new_segment2.blockers.append(((x1, y1), (x2, y2)))

        return new_segment1, new_segment2

    def split(self):
        sega, segb = self.split_x()
        seg1, seg2 = sega.split_y()
        seg3, seg4 = segb.split_y()
        return seg1, seg2, seg3, seg4

    def merge_translated_from(self, other, dx, dy):
        for (x1, y1), (x2, y2) in other.blockers:
            self.blockers.append(((x1 + dx, y1 + dy), (x2 + dx, y2 + dy)))
        for ((x1, y1), (x2, y2)), (user, bs) in other.links.items():
            self.links[((x1 + dx, y1 + dy), (x2 + dx, y2 + dy))] = (user, bs)


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
        self.points = (
        Point(self.x1, self.y1), Point(self.x2, self.y2), Point(self.x3, self.y3), Point(self.x4, self.y4))
        self.line_segments = [[(self.x1, self.y1), (self.x2, self.y2)],
                              [(self.x1, self.y1), (self.x4, self.y4)],
                              [(self.x3, self.y3), (self.x4, self.y4)],
                              [(self.x2, self.y2), (self.x3, self.y3)]]

        self.area = width * length


def simulate_blockers():
    max_area = 1 / 10 * xmax * ymax
    area = 0
    segment = Segment(xmin - xDelta, ymin - yDelta, xmax + xDelta, ymax + yDelta)

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


def distance(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def find_modified_coords(coord_1, coord_2):
    (x1, y1) = coord_1
    (x2, y2) = coord_2

    shift_x = [-xDelta, 0, xDelta]
    shift_y = [-yDelta, 0, yDelta]

    min_distance = math.inf
    shift = (0, 0)

    for sx in shift_x:
        for sy in shift_y:
            dist = distance(x1 + sx, y1 + sy, x2, y2)
            if dist <= min_distance:
                min_distance = dist
                shift = (sx, sy)

    return (x1 + shift[0], y1 + shift[1]), (x2, y2)

def counter_clockwise(xa, ya, xb, yb, xc, yc):
    return (yc - ya) * (xb - xa) > (yb - ya) * (xc - xa)

def intersect(xa, ya, xb, yb, xc, yc, xd, yd):
    return counter_clockwise(xa, ya, xc, yc, xd, yd) != counter_clockwise(xb, yb, xc, yc, xd, yd) and  counter_clockwise(xa, ya, xb, yb, xc, yc) != counter_clockwise(xa, ya, xb, yb, xd, yd)

def plot_blockers(blockers, ax):
    patchPoly = PolygonPatch(blockers)
    ax.add_patch(patchPoly)

def find_blocked_connections(opt_x, x_user, y_user, number_of_users):
    segments = segmentation(opt_x, x_user, y_user, number_of_users)
    connection_blocked = np.zeros((number_of_users, number_of_bs))
    for segment in segments:
        for ((x1, y1), (x2, y2)), (user, bs) in segment.links.items():
            lines = segment.blockers
            for ((x3, y3), (x4, y4)) in lines:
                if intersect(x1, y1, x2, y2, x3, y3, x4, y4):
                    connection_blocked[user, bs] = 1
    return connection_blocked


def segmentation(opt_x, x_user, y_user, number_of_users):
    segment = simulate_blockers()

    for i in range(number_of_users):
        for j in range(number_of_bs):
            if opt_x[i, j] > 0:
                coord1 = (x_user[i], y_user[i])
                coord2 = (x_bs[j], y_bs[j])

                coord1, coord2 = find_modified_coords(coord1, coord2)
                segment.links[coord1, coord2] = (i, j)

    # fix giant segment:
    left, temp = segment.split_x(mid_x=xmin)
    mid, right = temp.split_x(mid_x=xmax)

    mid.merge_translated_from(left, dx=xDelta, dy=0)
    mid.merge_translated_from(right, dx=-xDelta, dy=0)

    down, temp = mid.split_y(mid_y=ymin)
    mid, up = temp.split_y(mid_y=ymax)

    mid.merge_translated_from(down, dx=0, dy=yDelta)
    mid.merge_translated_from(up, dx=0, dy=-yDelta)

    to_split = [mid]
    finished = []
    while to_split:
        seg = to_split.pop(0)
        segments = seg.split()
        if sum(s.pair for s in segments) > seg.pair:
            finished.append(seg)
        else:
            for segment in segments:
                if not segment.is_empty:
                    if segment.pair > 1:
                        to_split.append(segment)
                    else:
                        finished.append(segment)
                    # print(segment.pair, len(to_split))
                    # print(segment.blockers)
                    # print(segment.links)

    return finished


if __name__ == '__main__':
    np.random.seed(1)
    x_user, y_user = f.find_coordinates(100)
    number_of_users = len(x_user)

    name = str(
        'users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(
            users_per_beam))
    optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))

    opt_x = optimal[0]

    start = time.time()
    segments = segmentation(opt_x, x_user, y_user, number_of_users)
    print(time.time() - start)

    fig, ax = plt.subplots()
    for i, seg in enumerate(segments):
        ax.add_patch(
            matplotlib.patches.Rectangle((seg.xmin, seg.ymin), width=seg.xmax - seg.xmin, height=seg.ymax - seg.ymin,
                                         alpha=0.1, color=colors[i]))
        for (x1, y1), (x2, y2) in seg.blockers:
            plt.plot([x1, x2], [y1, y2], color=colors[i])
        # for ((x1, y1), (x2, y2)), [user, bs] in seg.links.items():
        #     plt.plot([x1, x2], [y1, y2], color = colors[user])

    # plt.scatter(x_bs, y_bs, color='k')
    opt_x = optimal[0]

    plt.axis('off')
    plt.savefig('blocker_segmentation.png', dpi = 300)
    plt.show()
    np.random.seed(1)
    start = time.time()
    find_blocked_connections1(opt_x, x_user, y_user, number_of_users)
    print(time.time() - start)
