import pickle
import time
import matplotlib.patches
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import *
from parameters import *
# from svgpath2mpl import parse_path
import matplotlib as mpl

# Use Inkscape to edit SVG,
# Path -> Combine to convert multiple paths into a single path
# Use Path -> Object to path to convert objects to SVG path
# smiley = parse_path("""m 134.72756,172.59021 c -0.7217,0.16654 -1.20371,0.80044 -1.69003,1.30988 -1.26103,1.32097 -2.30226,2.84065 -3.23757,4.40266 -4.23765,7.07738 -4.55879,15.99828 -1.42138,23.53734 1.0491,2.52103 2.5924,4.91566 4.41595,6.94266 0.77665,0.86326 1.64525,1.95741 2.94903,1.49115 0.97104,-0.3473 1.42138,-1.59469 0.92498,-2.50715 -0.46524,-0.85521 -1.34789,-1.52755 -1.95758,-2.286 -1.13859,-1.41639 -2.13368,-2.99466 -2.87384,-4.65666 -2.79247,-6.27033 -2.74904,-13.71964 0.54593,-19.812 0.7311,-1.35188 1.57523,-2.62103 2.54974,-3.81 0.55778,-0.68047 1.41402,-1.30912 1.77952,-2.11667 0.59098,-1.30556 -0.56371,-2.82304 -1.98475,-2.49521 m 61.04466,0 c -1.10405,0.25298 -1.67471,1.45669 -1.22513,2.49521 0.47075,1.08543 1.72805,2.00406 2.44179,2.96333 4.95723,6.66259 5.76326,15.51585 2.31309,23.02934 -0.75014,1.63423 -1.75852,3.17838 -2.89136,4.572 -0.54018,0.66471 -1.24884,1.2324 -1.71789,1.94733 -0.80687,1.22978 0.10329,2.88984 1.5875,2.78579 0.84159,-0.059 1.32503,-0.70265 1.86351,-1.26179 1.34112,-1.39167 2.4384,-2.99839 3.41969,-4.65667 4.23587,-7.15992 4.57708,-16.6541 0.96012,-24.13 -1.09305,-2.25916 -2.45364,-4.3997 -4.14105,-6.26533 -0.67479,-0.74574 -1.4842,-1.73736 -2.61027,-1.47921 m -54.35599,5.68189 c -0.61308,0.17721 -1.08679,0.75151 -1.48802,1.21599 -0.8222,0.95174 -1.55406,1.95385 -2.17644,3.048 -2.78342,4.89348 -3.07179,11.0109 -0.84667,16.17133 0.77021,1.7863 1.83557,3.48446 3.16399,4.91067 0.68589,0.73634 1.46482,1.43103 2.53247,1.01981 1.25806,-0.48455 1.39387,-2.03192 0.577,-2.96715 -3.95486,-4.5278 -5.52179,-10.50764 -2.92151,-16.17133 0.54687,-1.19117 1.25045,-2.28363 2.074,-3.302 0.45212,-0.55914 1.15172,-1.04606 1.32613,-1.778 0.32267,-1.35458 -0.88967,-2.5378 -2.24095,-2.14732 m 47.32866,0 c -1.27678,0.36898 -1.50114,1.97299 -0.73406,2.90932 0.97282,1.18711 1.94818,2.2617 2.65938,3.64067 2.01168,3.89924 2.16577,8.61644 0.33443,12.61533 -0.49869,1.08949 -1.12607,2.11159 -1.87452,3.048 -0.47159,0.59097 -1.20989,1.14105 -1.47489,1.86267 -0.4445,1.21124 0.53678,2.57894 1.85166,2.39987 1.73651,-0.23647 3.28676,-3.01726 4.04452,-4.43187 2.68394,-5.01244 3.1623,-11.3312 0.59098,-16.51 -0.79248,-1.59707 -1.70011,-3.06011 -2.88206,-4.40267 -0.6604,-0.75006 -1.44272,-1.44145 -2.51544,-1.13132 m -23.79133,3.11455 c -2.09305,0.275 -4.00152,0.84244 -5.67267,2.20472 -1.0397,0.8476 -1.93133,1.90526 -2.55854,3.09338 -3.81271,7.22232 2.27872,15.87983 10.34787,14.79279 1.41986,-0.19134 2.76522,-0.71788 3.97933,-1.46727 7.23138,-4.46481 5.52704,-15.60525 -2.37066,-18.17946 -1.14385,-0.37278 -2.52476,-0.60181 -3.72533,-0.44416 m -16.51,2.45906 c -1.10897,0.21141 -1.89772,1.52095 -2.43806,2.41571 -1.72348,2.85386 -1.87943,6.55896 -0.45915,9.56733 0.61968,1.31268 1.89814,3.66412 3.65921,3.25721 0.98569,-0.22783 1.5621,-1.28727 1.26534,-2.24121 -0.22597,-0.72652 -0.89577,-1.23588 -1.30395,-1.86266 -0.71941,-1.10482 -1.17458,-2.56659 -1.04766,-3.89467 0.10955,-1.14715 0.47277,-2.25713 1.11666,-3.21733 0.47549,-0.70917 1.27077,-1.28787 1.31539,-2.20134 0.0561,-1.14825 -0.98256,-2.0375 -2.10778,-1.82304 m 33.69733,0 c -0.99822,0.18703 -1.62222,1.1767 -1.39446,2.16171 0.17018,0.73584 0.87122,1.25383 1.27931,1.86267 0.69765,1.04047 1.15062,2.37651 1.12691,3.64066 -0.0237,1.22014 -0.41317,2.44873 -1.07103,3.47134 -0.48006,0.74684 -1.31403,1.34306 -1.37245,2.286 -0.0686,1.12352 0.92964,1.98204 2.02438,1.847 1.14808,-0.14165 1.97782,-1.53772 2.52307,-2.43967 1.73736,-2.8768 1.87452,-6.73075 0.37169,-9.73667 -0.61807,-1.23689 -1.82965,-3.40385 -3.48742,-3.09304 m -17.10266,1.08526 c 6.71744,-0.8034 9.75274,8.6636 4.06399,12.1285 -0.82126,0.50029 -1.75514,0.82914 -2.70933,0.9464 -6.64574,0.81619 -10.0556,-8.33797 -4.40266,-12.00988 0.93361,-0.60647 1.94758,-0.93345 3.048,-1.06502 m -3.81,21.6198 c -1.0917,0.31555 -1.27517,1.53916 -1.51325,2.48598 -0.59826,2.37812 -1.28592,4.7338 -1.88417,7.112 -2.49852,9.93293 -5.2015,19.83063 -7.87604,29.718 -2.53856,9.38446 -4.87087,18.82733 -7.47378,28.194 -0.66446,2.39099 -1.2297,4.81076 -1.91143,7.19667 -0.27551,0.96435 -0.8581,2.24367 -0.40733,3.21733 0.55736,1.20481 1.93446,1.016 3.032,1.016 h 8.55133 26.75466 7.874 c 1.12945,0 2.6543,0.26501 3.72533,-0.11768 2.0828,-0.74422 0.72644,-3.67962 0.31412,-5.13165 -1.45034,-5.11133 -2.66531,-10.29039 -4.08856,-15.40933 -3.78968,-13.63811 -7.28302,-27.37358 -10.88305,-41.06334 -1.00923,-3.83921 -2.08026,-7.66495 -3.04885,-11.51466 -0.29802,-1.18745 -0.61044,-2.37804 -0.94488,-3.556 -0.15494,-0.54627 -0.2269,-1.15367 -0.60113,-1.60503 -0.61722,-0.74388 -1.55956,-0.59631 -2.42231,-0.59631 h -4.826 c -0.73423,0 -1.66217,-0.1507 -2.37066,0.054 m -1.10067,14.67798 c 0.74938,-2.64075 1.42849,-5.30394 2.12649,-7.95866 0.21056,-0.80087 0.33451,-2.56871 0.90915,-3.16628 0.34882,-0.36263 1.65159,-0.13572 2.12903,-0.13572 0.72389,0 2.02776,-0.25417 2.68562,0.0511 0.25485,0.11811 0.29125,0.46982 0.35137,0.71095 0.16933,0.67039 0.76369,1.86309 0.61214,2.54 -0.17526,0.77851 -1.70858,1.70984 -2.29447,2.22554 -1.36296,1.19982 -2.71424,2.41597 -4.064,3.63077 -0.77792,0.7001 -1.54694,1.57734 -2.45533,2.10235 m 9.398,-5.92666 4.40266,16.51 c -1.59427,-0.28448 -3.26982,-1.49945 -4.74133,-2.17517 -3.31047,-1.51994 -6.84538,-2.93176 -9.99066,-4.7675 0.24849,-1.13851 1.94056,-2.17466 2.794,-2.91457 2.47582,-2.14663 4.80313,-4.84547 7.53533,-6.65276 m 4.48733,18.62666 c -4.48903,2.74744 -9.0794,5.35263 -13.63133,7.99423 -2.13834,1.24121 -4.36728,3.01413 -6.68867,3.85911 l 1.44916,-5.67267 3.54618,-13.462 c 1.23266,0.33714 2.40317,1.08272 3.556,1.62721 2.17483,1.02726 4.3544,2.04453 6.51933,3.09211 1.6383,0.79248 3.84809,1.40123 5.24933,2.56201 m 0.84666,1.524 2.10651,7.874 4.32816,16.256 c -1.03886,-0.17864 -2.07179,-0.77808 -3.048,-1.1684 -2.14884,-0.85936 -4.28583,-1.74836 -6.43467,-2.60773 -6.18997,-2.4765 -12.58899,-4.74472 -18.62666,-7.5692 l 2.70934,-1.68063 4.99533,-2.92693 9.31333,-5.46862 4.65666,-2.70849 m 6.604,26.162 c -1.04817,0.98129 -2.79992,1.54432 -4.064,2.22758 -2.7813,1.50368 -5.58546,2.96672 -8.38199,4.44246 -5.70569,3.01075 -11.3969,6.04859 -17.10267,9.05934 -2.56193,1.35212 -5.08025,2.8575 -7.70466,4.08262 0.44102,-2.99804 1.56616,-6.04774 2.35788,-8.97466 1.3567,-5.01566 2.66116,-10.0457 3.98229,-15.07067 0.65092,-2.47565 1.43968,-4.94369 1.95716,-7.45067 l 3.13267,1.18534 6.43466,2.60773 13.37733,5.43475 6.01133,2.45618 m 0.84667,1.69334 1.84997,7.112 3.0607,11.51466 h -40.132 c 0.7863,-0.6587 1.88443,-1.07611 2.794,-1.54601 1.50216,-0.77555 3.00033,-1.57057 4.48734,-2.3749 5.6189,-3.03869 11.31485,-5.93598 16.93332,-8.97467 2.35966,-1.27592 4.76589,-2.47142 7.112,-3.7719 1.14554,-0.635 2.6052,-1.72889 3.89467,-1.95918 z""")
# smiley.vertices -= smiley.vertices.mean(axis=0)
# smiley = smiley.transformed(mpl.transforms.Affine2D().rotate_deg(180))

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
        width, length = np.random.uniform(5, 50), np.random.uniform(5, 50)
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
    number_of_users = 600
    name = str(
        'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(M) + 's=' + str(
            users_per_beam) + 'rate=500')

    optimal = pickle.load(open(str('Data/assignment1' + name + '.p'), 'rb'))
    x_user = pickle.load(open(str('Data/xs1' + name + '.p'), 'rb'))
    y_user = pickle.load(open(str('Data/ys1' + name + '.p'), 'rb'))

    x_user, y_user = x_user[0], y_user[0]
    opt_x = optimal[0]

    start = time.time()
    segments = segmentation(opt_x, x_user, y_user, number_of_users)
    print(time.time() - start)

    fig, ax = plt.subplots()
    # for i, seg in enumerate(segments):
        # ax.add_patch(
        #     matplotlib.patches.Rectangle((seg.xmin, seg.ymin), width=seg.xmax - seg.xmin, height=seg.ymax - seg.ymin,
        #                                  alpha=0.1, color=colors[i]))
        # for (x1, y1), (x2, y2) in seg.blockers:
        #     plt.plot([x1, x2], [y1, y2], color=colors[i])
        # for ((x1, y1), (x2, y2)), [user, bs] in seg.links.items():
        #     plt.plot([x1, x2], [y1, y2], color = colors[user])
    blockers = simulate_blockers()
    i = 0
    k = 0
    for (x1, y1), (x2, y2) in blockers.blockers:
        plt.plot([x1 * 10, x2 * 10], [y1 * 10, y2 * 10], color=colors[3])
        i += 1
        if i % 4 == 0:
            k += 1
    plt.scatter([x*10 for x in x_bs], [y * 10 for y in y_bs], marker = smiley, color='k', s = 1000)
    opt_x = optimal[0]

    plt.axis('off')
    # print(min(x_bs), max(x_bs), min(y_bs), max(y_bs))
    plt.xlim((1900, 5300))
    plt.ylim((-500, 2200))
    plt.savefig('blocker_segmentation.png', dpi = 300)
    plt.show()
    np.random.seed(1)
    start = time.time()
    # find_blocked_connections(opt_x, x_user, y_user, number_of_users)
    print(time.time() - start)
