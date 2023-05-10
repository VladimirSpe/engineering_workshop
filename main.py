from Inp_Rea import Read_Json
from Littles_method import Main_Method
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

COLORS = list(mcolors.BASE_COLORS.keys())


def main():
    fig, ax = plt.subplots()
    geom = Read_Json("tests/file_kt_1.json")
    geom.draw(ax)
    geom.preparation()
    print(geom.matrix)
    res = Main_Method("", geom.matrix, 1, 1)
    draw_mat = geom.path_matrix
    print(res.solution_cycle())
    for path in res.solution_cycle()[0]:
        draw_mat[int(path[0])][int(path[1])].draw(ax)

    ax.set_aspect('equal')
    plt.show()


if __name__ == '__main__':
    main()
