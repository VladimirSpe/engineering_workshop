import json
import numpy as np
import params
import math


class Read_Json:
    def __init__(self, file_name, file_SVN):
        """Read JSON files"""
        self.SVN_names = []
        self.SVN_cords = []
        if file_SVN != "":
            with open(file_SVN) as f:
                self.SVN_names = json.load(f)
        with open(file_name) as f:
            self.data = json.load(f)
        self.circles = []
        self.matrix = np.zeros((len(self.data), len(self.data)))

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
            if (id1 == self.SVN_names[i][0] and id2 == self.SVN_names[i][1]) or (
                    id1 == self.SVN_names[i][1] and id2 == self.SVN_names[i][0]):
                return True
        return False

    def check_w_circle(self, point1, point2):
        """Check intersection with Сircles"""
        A_x, A_y = point1
        B_x, B_y = point2
        for i in self.circles:
            # vert_x, vert_y = i["x"], i["y"]
            r = i["r"]
            b = 2 * (A_x(B_x - A_x) + A_y(B_y - A_y))
            a = ((B_x - A_x) ** 2 + (B_y - A_y) ** 2)
            c = (A_x ** 2 + A_y ** 2 - r ** 2)
            D = b ** 2 - 4 * a * c
            if D >= 0:
                return True
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

    def preparation(self):
        """Creating matrix"""
        self.find_cords_by_name()
        for i in range(len(self.data)):
            x1 = self.data[i]["x"]
            y1 = self.data[i]["y"]
            id1 = self.data[i]["id"]
            self.matrix[i][i] = np.inf
            for j in range(0, i):
                x2 = self.data[j]["x"]
                y2 = self.data[j]["y"]
                id2 = self.data[j]["id"]

                if self.check_w_SVN(id1, id2) is False:
                    self.matrix[i][j] = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                    self.matrix[j][i] = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                else:
                    self.matrix[i][j] = np.inf
                    self.matrix[j][i] = np.inf
        return self.matrix

    def get_matrix(self):
        return self.matrix

