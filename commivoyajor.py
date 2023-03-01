import numpy as np

class Commivoyajor:
    def __init__(self, arr):
        self.arr = arr
        self.dags = np.array()
        self.solution = np.array()
        self.H = 0
        self.H_w_edge = 0
        self.H2_wo_edge = 0

    def reduction_lines(self):
        lines_min = []
        for i in self.arr:
            min_iter = min(i)
            for k in i:
                k -= min_iter
            lines_min.append(min_iter)
        self.H += sum(lines_min)

    def reduction_columns(self):
        self.arr.transpose()
        self.reduction_lines()
        self.arr.transpose()

    def nulls_degree(self):
        pass

    def src_max_degree(self):
        pass

    def remove_line(self):
        pass

    def remove_column(self):
        pass

    def compare_solutions(self):
        pass

    def compare_w_daglings(self):
        pass