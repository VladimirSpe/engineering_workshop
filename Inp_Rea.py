import json
import math

import numpy as np
import params
from math import atan2, acos, sin, cos, sqrt, asin
from matplotlib.patches import Circle, Arc
import matplotlib.patches


class LineTour:
    def __init__(self, id1, id2, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.L = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
        self.id1 = id1
        self.id2 = id2

    def get_length(self):
        return self.L

    def draw(self, ax):
        line = matplotlib.patches.Polygon([self.p1, self.p2], fill=False, closed=False, color="green")
        ax.add_patch(line)


class CircleTour:
    def __init__(self, id1_p, id2_p):
        self.tang1 = (0, 0)
        self.tang2 = (0, 0)
        self.L = 0
        self.id1_p = id1_p
        self.id2_p = id2_p
        self.center = (0, 0)
        self.r = 0

    def build_circle_detour(self, point1, point2, circle_point, r):
        tangents1 = self.build_tangent(point1, circle_point, r)
        tangents2 = self.build_tangent(point2, circle_point, r)
        arc11 = self.arc_length(tangents1[0], tangents2[0], r)
        arc12 = self.arc_length(tangents1[0], tangents2[1], r)
        arc21 = self.arc_length(tangents1[1], tangents2[0], r)
        arc22 = self.arc_length(tangents1[1], tangents2[1], r)
        way1 = tangents1[2] + tangents2[2] + arc11
        way2 = tangents1[2] + tangents2[2] + arc12
        way3 = tangents1[2] + tangents2[2] + arc21
        way4 = tangents1[2] + tangents2[2] + arc22
        min_way = min(way1, way2, way3, way4)
        self.center = circle_point
        self.r = r
        if way1 == min_way:
            self.tang1 = tangents1[0]
            self.tang2 = tangents2[0]
            self.L = way1
        if way2 == min_way:
            self.tang1 = tangents1[0]
            self.tang2 = tangents2[1]
            self.L = way2
        if way3 == min_way:
            self.tang1 = tangents1[1]
            self.tang2 = tangents2[0]
            self.L = way3
        if way4 == min_way:
            self.tang1 = tangents1[1]
            self.tang2 = tangents2[1]
            self.L = way4

    def build_tangent(self, point, point_circle, R):
        A_x, A_y = point
        C_x, C_y = point_circle
        l_x = C_x - A_x
        l_y = C_y - A_y
        l = (l_x ** 2 + l_y ** 2) ** 0.5
        T1_x = R * sin(atan2(l_y, l_x) - asin(R / l)) + C_x
        T1_y = R * (-cos(atan2(l_y, l_x) - asin(R / l))) + C_y
        T2_x = R * (-sin(atan2(l_y, l_x) + asin(R / l))) + C_x
        T2_y = R * (cos(atan2(l_y, l_x) + asin(R / l))) + C_y
        return (T1_x, T1_y), (T2_x, T2_y), l

    def angle_btw_points(self, point1, point2, radius):
        L = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        alpha = acos(1 - ((L ** 2) / (2 * (radius ** 2))))
        return alpha

    def arc_length(self, point1, point2, radius):
        return radius * self.angle_btw_points(point1, point2, radius)

    def get_length(self):
        return self.L
    def draw(self, ax):
        angle1 = np.arctan2(self.tang1[1] - self.center[1], self.tang1[0] - self.center[0])
        angle2 = np.arctan2(self.tang2[1] - self.center[1], self.tang2[0] - self.center[0])

        # находим разницу углов и считаем длину дуги
        arc_length = self.r * np.abs(angle2 - angle1)

        # создаем объект дуги
        arc = Arc(self.center, 2 * self.r, 2 * self.r, angle=0, theta1=min(np.degrees(angle1), np.degrees(angle2)), theta2=max(np.degrees(angle1), np.degrees(angle2)),
                  color="green")

        ax.add_patch(arc)
        line1 = matplotlib.patches.Polygon([self.id1_p, self.tang1], fill=False, closed=False, color="green")
        line2 = matplotlib.patches.Polygon([self.id2_p, self.tang2], fill=False, closed=False, color="green")

        ax.add_patch(line1)
        ax.add_patch(line2)


class Read_Json:
    def __init__(self, file_name):
        """Read JSON files"""

        with open(file_name) as f:
            self.data = json.load(f)
        self.KT = self.data["data_points"]
        self.SVN_names = self.data["forbidden_lines"]
        self.SVN_cords = []
        self.circles = self.data["data_forbidden_zone"]
        self.matrix = np.zeros((len(self.KT), len(self.KT)))
        self.path_matrix = [[None] * len(self.KT) for i in range(len(self.KT))]

    def find_cords_by_name(self):
        for i in range(len(self.SVN_names)):
            id1_cords = (0, 0)
            id2_cords = (0, 0)
            for j in range(len(self.KT)):
                if self.SVN_names[i]["id1"] == self.KT[j]["id"]:
                    id1_cords = (self.KT[j]["x"], self.KT[j]["y"])
                if self.SVN_names[i]["id2"] == self.KT[j]["id"]:
                    id2_cords = (self.KT[j]["x"], self.KT[j]["y"])
            self.SVN_cords.append((id1_cords, id2_cords))

    def orientation(self, a, b, c):
        """
        Check orientation:
                0 - collenary,
                1-  clockwise,
                2 - counter-clockwise
        """
        t = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
        if t == 0:
            return 0
        elif t > 0:
            return 1
        else:
            return 2

    def check_intersection(self, sec1, sec2):
        p1 = self.orientation(sec1[0], sec1[1], sec2[0]) != self.orientation(sec1[0], sec1[1], sec2[1])
        p2 = self.orientation(sec2[0], sec2[1], sec1[0]) != self.orientation(sec2[0], sec2[1], sec1[1])
        if p1 and p2:
            return True
        return False

    def check_w_SVN(self, id1, id2):
        """Check intersection with SVN"""
        for i in range(len(self.SVN_names)):
            if (id1 == self.SVN_names[i]["id1"] and id2 == self.SVN_names[i]["id2"]) or (
                    id1 == self.SVN_names[i]["id2"] and id2 == self.SVN_names[i]["id1"]):
                return True
        return False

    def check_w_circle(self, A, B):
        for i in self.circles:
            C = (i["x"], i["y"])
            R = i["r"]
            Ax, Ay = A[0] - C[0], A[1] - C[1]
            Bx, By = B[0] - C[0], B[1] - C[1]

            a = (Bx - Ax) ** 2 + (By - Ay) ** 2
            b = 2 * (Ax * (Bx - Ax) + Ay * (By - Ay))
            c = Ax ** 2 + Ay ** 2 - R ** 2
            d = b ** 2 - 4 * a * c
            if d < 0:
                continue
            t1 = (-b - sqrt(d)) / (2 * a)
            t2 = (-b + sqrt(d)) / (2 * a)
            if 0 <= t1 <= 1 or 0 <= t2 <= 1:
                return True, C, R
            else:
                continue
        return False

    def preparation(self):
        """Creating matrix"""
        ids = [0]
        for i in range(len(self.KT)):
            x1 = self.KT[i]["x"]
            y1 = self.KT[i]["y"]
            id1 = self.KT[i]["id"]
            self.matrix[i][i] = np.inf
            ids.append(id1)
            for j in range(0, i):
                x2 = self.KT[j]["x"]
                y2 = self.KT[j]["y"]
                id2 = self.KT[j]["id"]
                p1 = self.check_w_SVN(id1, id2)
                p2 = self.check_w_circle((x1, y1), (x2, y2))
                if p1 is False and p2 is False:
                    line = LineTour(id1, id2, (x1, y1), (x2, y2))
                    self.matrix[i][j] = line.get_length()
                    self.matrix[j][i] = line.get_length()
                    self.path_matrix[i][j] = line
                    self.path_matrix[j][i] = line
                elif p1 is True:
                    self.matrix[i][j] = np.inf
                    self.matrix[j][i] = np.inf
                elif p2[0] is True:
                    circ = CircleTour((x1, y1), (x2, y2))
                    circ.build_circle_detour((x1, y1), (x2, y2), p2[1], p2[2])
                    S = circ.get_length()
                    self.matrix[i][j] = S
                    self.matrix[j][i] = S
                    self.path_matrix[i][j] = circ
                    self.path_matrix[j][i] = circ
        self.path_matrix = np.vstack([np.array(ids)[1:], self.path_matrix])
        self.matrix = np.vstack([np.array(ids)[1:], self.matrix])
        ids = np.array(ids).reshape(len(ids), 1)
        self.path_matrix = np.hstack([ids, self.path_matrix])
        self.matrix = np.hstack([ids, self.matrix])

        return self.matrix

    def draw(self, ax):
        for i in self.KT:
            ax.scatter(i["x"], i["y"], label=i["id"])

        for i in self.circles:
            C = (i["x"], i["y"])
            R = i["r"]
            id = i["id"]
            ax.add_patch(Circle((C[0], C[1]), R, fill=False, linewidth=2, color="red",
                                label=id))
            self.find_cords_by_name()
        for i in self.SVN_cords:
            line = matplotlib.patches.Polygon([i[0], i[1]],
                                              fill=False,
                                              closed=False,
                                              color="red")
            ax.add_patch(line)

        def get_matrix(self):
            return self.matrix

