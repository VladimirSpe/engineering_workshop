from Inp_Rea import Read_Json
from Littles_method import Main_Method
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

COLORS = list(mcolors.BASE_COLORS.keys())


def main():
    fig, ax = plt.subplots()
    geom = Read_Json("tests/test_mtsp2.json")
    geom.draw(ax)
    geom.preparation()
    res = Main_Method("", geom.matrix, geom.start_coord, geom.number_bpla)
    draw_mat = geom.path_matrix
    print(res.solution_cycle())
    if geom.number_bpla == 1:
        for path in res.solution_cycle()[0]:
            draw_mat[int(path[0])][int(path[1])].draw(ax)
    else:
        for bpla in range(geom.number_bpla):
            for path in res.solution_cycle()[0][bpla]:
                draw_mat[int(path[0])][int(path[1])].draw(ax, COLORS[bpla])
    ax.set_aspect('equal')
    plt.show()


if __name__ == '__main__':
    main()
