from Littles_method import Main_method
import matplotlib.pyplot as plt
import json
from Inp_Rea import Read_Json


def index_to_coord(data, points):
    l_x = []
    l_y = []
    for i in range(len(points)):
        for j in range(len(data)):

            if points[i][0] == data[j]["id"]:
                l_x.append([data[j]["x"], data[j]["y"]])
            if points[i][1] == data[j]["id"]:
                l_y.append((data[j]["x"], data[j]["y"]))
    return l_x, l_y


def main():
    file = Read_Json("file_kt_1.json", "")
    mat = Main_method(1, file.preparation())
    coords = mat.solution_cycle()[0]
    l_x, l_y = index_to_coord(file.data, coords)
    plt.plot(l_x, l_y)
    plt.show()


if __name__ == '__main__':
    main()
