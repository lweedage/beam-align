import functions as f
from parameters import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches
from shapely.geometry import *

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

        self.coords = [[self.x1, self.y1], [self.x2, self.y2], [self.x3, self.y3], [self.x4, self.y4]]
        self.points = (
        Point(self.x1, self.y1), Point(self.x2, self.y2), Point(self.x3, self.y3), Point(self.x4, self.y4))
        self.line_segments = [LineString([(self.x1, self.y1), (self.x2, self.y2)]),
                              LineString([(self.x1, self.y1), (self.x4, self.y4)]),
                              LineString([(self.x3, self.y3), (self.x4, self.y4)])]
        self.area = width * length

        # self.poly = Polygon(*self.points)


def simulate_blockers():
    max_area = 1 / 10 * xmax * ymax
    area = 0

    rectangles = [[] for i in range(2 ** (2 * subdivisions))]
    print(rectangles, len(rectangles))
    while area < max_area:
        x_c, y_c = np.random.uniform(0, xmax), np.random.uniform(0, ymax)
        width, length = np.random.uniform(1, 25), np.random.uniform(1, 25)
        angle = np.random.uniform(0, 2 * math.pi)
        rectangle = Rectangle(x_c, y_c, angle, length, width)
        area += rectangle.area
        for segment in rectangle.line_segments:
            first, last = segment.boundary
            part1 = find_which_part((first.x, first.y))
            part2 = find_which_part((last.x, last.y))

            rectangles[part1].append(segment)
            if part1 != part2:
                rectangles[part2].append(segment)
    return rectangles


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


def find_modified_blockers(coord_1, blockers):
    for i in range(len(blockers)):
        for j in range(len(blockers[i])):
            first, last = blockers[i][j].boundary
            center_coord = ((first.x + last.x) / 2, (first.y + last.y) / 2)
            (x1, y1) = (first.x, first.y)
            (x2, y2) = (last.x, last.y)

            if (max(center_coord[0], coord_1[0]) - min(center_coord[0], coord_1[0])) > (
                    min(center_coord[0], coord_1[0]) - max(center_coord[0], coord_1[0])) % xDelta:
                if center_coord[0] > coord_1[0]:
                    x1 += xDelta
                    x2 += xDelta
                else:
                    x1 -= xDelta
                    x2 -= xDelta

            if (max(center_coord[1], coord_1[1]) - min(center_coord[1], coord_1[1])) > (
                    min(center_coord[1], coord_1[1]) - max(center_coord[1], coord_1[1])) % yDelta:
                if center_coord[1] > coord_1[1]:
                    y1 += yDelta
                    y2 += yDelta
                else:
                    y1 -= yDelta
                    y2 -= yDelta

            blockers[i][j] = LineString([(x1, y1), (x2, y2)])
    return blockers


def is_connection_blocked(user, bs, blockers):
    # if Torus:
    #     user, bs = f.find_modified_coords(user, bs)
    no_intersect = True
    part1 = find_which_part(user)
    part2 = find_which_part(bs)

    i = 0
    if part1 != part2:
        user = find_modified_coords(user, bs)
        blockers = find_modified_blockers(bs, blockers)
    s = LineString([user, bs])

    while no_intersect and i < len(blockers[part1]):
        no_intersect = not s.intersects(blockers[part1][i])
        i += 1

    if part1 != part2:
        if (part1 - part2) % 5 != 0:
            for part1 in range(len(blockers)):
                while no_intersect and i < len(blockers[part1]):
                    no_intersect = not s.intersects(blockers[part1][i])
                    i += 1

        else:
            while no_intersect and i < len(blockers[part2]):
                no_intersect = not s.intersects(blockers[part2][i])
                i += 1
    return not no_intersect


if __name__ == '__main__':
    blockers = simulate_blockers()
    #
    # fig, ax = plt.subplots()
    # draw_blockers(blockers, ax)
    # plt.xlim([0, xmax])
    # plt.ylim([0, ymax])
    # plt.show()
    bs = (10, 20)
    x_user, y_user = f.find_coordinates(100)

    for u in range(len(x_user)):
        user = (x_user[u], y_user[u])
        print(is_connection_blocked(user, bs, blockers))
