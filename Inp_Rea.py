import json


class Read_Json:
    def __init__(self, file_name, file_SVN):
        """Read JSON files"""
        self.matrix = []
        self.SVN_names = []
        self.SVN_cords = []

        with open(file_SVN) as f:
            self.SVN_names = json.load(f)
        with open(file_name) as f:
            self.data = json.load(f)

    def find_cords_by_name(self):
        """Danger Zone's JSON have only KT's id. This func get cords from id"""
        for i in range(len(self.SVN_names)):
            id1_cords = (0, 0)
            id2_cords = (0, 0)
            for j in range(len(self.data)):
                if self.SVN_names[i]["id1"] == self.data[j]["id"]:
                    id1_cords = (self.data[j]["x"], self.data[j]["y"])
                if self.SVN_names[i]["id2"] == self.data[j]["id"]:
                    id2_cords = (self.data[j]["x"], self.data[j]["y"])
            self.SVN_cords.append((id1_cords, id2_cords))

    def orientation(self, a, b, c):
        """Check orientation: 
        0 - collenary,
        1- clockwise,
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
        p1 = self.orientation(sec1[0], sec2[0], sec1[1]) != self.orientation(sec1[0], sec2[0], sec2[1])
        p2 = self.orientation(sec1[1],sec2[1],sec2[0]) != self.orientation(sec1[1],sec2[1],sec1[0])
        if p1 and p2:
            return True
        return False

    def preparation(self):
        """Creating matrix"""
        for k in range(len(self.SVN_cords)):
            dz_point1 = self.SVN_cords[k][0]
            dz_point2 = self.SVN_cords[k][1]
            for i in range(len(self.data)):
                m = []
                x = self.data[i]["x"]
                y = self.data[i]["y"]
                for j in range(len(self.data)):
                    if i != j and self.check_intersection((dz_point1, dz_point2), ((x, y), (self.data[j]["x"], self.data[j]["y"]))) != False:
                        m.append(((x - self.data[j]["x"]) ** 2 + (y - self.data[j]["y"]) ** 2) ** 0.5)
                    else:
                        m.append(1e100)
                self.matrix.append(m[:])
            return self.matrix

    def get_matrix(self):
        return self.matrix
