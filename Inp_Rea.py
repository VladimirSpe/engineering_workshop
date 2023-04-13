import json
import numpy as np
import params
import math


class Read_Json:
    def __init__(self, file_name):
        """Read JSON files"""

        with open(file_name) as f:
            self.data = json.load(f)
        self.KT = self.data["data_points"]
        self.SVN_names = self.data["forbidden_lines"]
        self.circles = self.data["data_forbidden_zone"]
        self.matrix = np.zeros((len(self.KT), len(self.KT)))
        # paths[i] = [id1, id2, mode, ...]
        self.paths = []

    """
    def find_cords_by_name(self):
        for i in range(len(self.SVN_names)):
            id1_cords = (0, 0)
            id2_cords = (0, 0)
            for j in range(len(self.data)):
                if self.SVN_names[i]["id1"] == self.data[j]["id"]:
                    id1_cords = (self.data[j]["x"], self.data[j]["y"])
                if self.SVN_names[i]["id2"] == self.data[j]["id"]:
                    id2_cords = (self.data[j]["x"], self.data[j]["y"])
            self.SVN_cords.append((id1_cords, id2_cords))
    """

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

    def check_w_circle(self, point1, point2):
        """Check intersection with Сircles"""
        A_x, A_y = point1
        B_x, B_y = point2
        for i in self.circles:
            vert_x, vert_y = i["x"], i["y"]
            r = i["r"]
            b = 2 * (A_x * (B_x - A_x) + A_y * (B_y - A_y))
            a = ((B_x - A_x) ** 2 + (B_y - A_y) ** 2)
            c = (A_x ** 2 + A_y ** 2 - r ** 2)
            D = b ** 2 - 4 * a * c
            if D >= 0:
                return True, (vert_x, vert_y), r
            else:
                return False

    def build_tangent(self, point, point_circle, R):
        A_x, A_y = point
        C_x, C_y = point_circle
        l_x = C_x - A_x
        l_y = C_y - A_y
        l = (l_x ** 2 + l_y ** 2) ** 0.5
        T1_x = R * math.sin(math.atan2(l_y, l_x) ** 2 - math.asin(R / l)) + C_x
        T1_y = R * (-math.cos(math.atan2(l_y, l_x) ** 2 - math.asin(R / l))) + C_y
        T2_x = R * (-math.sin(math.atan2(l_y, l_x) ** 2 - math.asin(R / l))) + C_x
        T2_y = R * (math.cos(math.atan2(l_y, l_x) ** 2 - math.asin(R / l))) + C_y
        return (T1_x, T1_y), (T2_x, T2_y), l

    def calculate_arc_length(self, point1, point2, r):
        a = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        return 2 * r * math.asin(a / (2 * r))

    def build_circle_detour(self, point1, point2, circle_point, r):
        tangents1 = self.build_tangent(point1, circle_point, r)
        tangents2 = self.build_tangent(point2, circle_point, r)
        arc11 = self.calculate_arc_length(tangents1[0], tangents2[0], r)
        arc12 = self.calculate_arc_length(tangents1[0], tangents2[1], r)
        arc21 = self.calculate_arc_length(tangents1[1], tangents2[0], r)
        arc22 = self.calculate_arc_length(tangents1[1], tangents2[1], r)
        way1 = tangents1[2] + tangents2[2] + arc11
        way2 = tangents1[2] + tangents2[2] + arc12
        way3 = tangents1[2] + tangents2[2] + arc21
        way4 = tangents1[2] + tangents2[2] + arc22
        min_way = min(way1, way2, way3, way4)

        if way1 == min_way:
            return tangents1[0], tangents2[0], way1
        if way2 == min_way:
            return tangents1[0], tangents2[1], way2
        if way3 == min_way:
            return tangents1[1], tangents2[0], way3
        if way4 == min_way:
            return tangents1[1], tangents2[1], way4

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
                    self.matrix[i][j] = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                    self.matrix[j][i] = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                    # [id1, id2, mod, p1, p2]
                    self.paths.append([id1, id2, "line", (x1, y1), (x2, y2)])
                elif p1 is True:
                    self.matrix[i][j] = np.inf
                    self.matrix[j][i] = np.inf
                elif p2[0] is True:
                    dot1, dot2, S = self.build_circle_detour((x1, y1), (x2, y2), p2[1], p2[2])
                    self.matrix[i][j] = S
                    self.matrix[j][i] = S
                    # [id1, id2, mode, point1, point2, point_tangent1, point_tangent2, circle_point, r_circle]
                    self.paths.append([id1, id2, "circle", (x1, y1), (x2, y2), dot1, dot2, p2[1], p2[2]])
        self.matrix = np.vstack([np.array(ids)[1:], self.matrix])
        ids = np.array(ids).reshape(len(ids), 1)
        self.matrix = np.hstack([ids, self.matrix])

        return self.matrix

    def get_matrix(self):
        return self.matrix



