from Inp_Rea import Read_Json
import matplotlib.pyplot as plt


def index_to_coord(vector_list, ind):
    coord_list_x = []
    coord_list_y = []
    for i in vector_list:
        coord_list_x.append(ind[i[0]][1])
        coord_list_y.append(ind[i[0]][2])
    coord_list_x.append(ind[vector_list[0][0]][1])
    coord_list_y.append(ind[vector_list[0][0]][2])
    return coord_list_x, coord_list_y


def main():
    mat = Read_Json("inp.json")
    ff = mat.preparation()
    coords = [(0, 2), (2, 1), (1, 0)]
    matrix, indexes = ff[0], ff[1]
    l_x, l_y = index_to_coord(coords, indexes)
    plt.plot(l_x, l_y)
    plt.show()


if __name__ == '__main__':
    main()
