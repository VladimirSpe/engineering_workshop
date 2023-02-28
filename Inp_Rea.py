import json


class Read_Json:
    def __init__(self, file_name):
        self.matrix = []
        with open(file_name) as f:
            self.data = json.load(f)

    def preparation(self):
        for i in range(len(self.data)):
            m = []
            x = self.data[i]["x"]
            y = self.data[i]["y"]
            for j in range(len(self.data)):
                if i != j:
                    m.append(((x - self.data[j]["x"]) ** 2 + (y - self.data[j]["y"]) ** 2)**0.5)
                else:
                    m.append(1e100)
            self.matrix.append(m[:])
        return self.matrix

    def get_matrix(self):
        return self.matrix
