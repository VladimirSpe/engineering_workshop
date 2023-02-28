from Inp_Rea import Read_Json


def main():
    mat = Read_Json("inp.json")
    print(mat.preparation())


if __name__ == '__main__':
    main()
