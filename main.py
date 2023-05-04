from Inp_Rea import Read_Json
from Littles_method import Main_Method
import matplotlib.pyplot as plt


def main():
    fig, ax = plt.subplots()
    geom = Read_Json("file_kt_1.json")
    geom.draw(ax)
    geom.preparation()
    res = Main_Method("", geom.matrix, 0)
    draw_mat = geom.path_matrix
    for path in res.solution_cycle()[0]:
        draw_mat[int(path[0])][int(path[1])].draw(ax)
    ax.set_aspect('equal')
    plt.show()


if __name__ == '__main__':
    main()
