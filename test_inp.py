from Inp_Rea import Read_Json
import params

class TestBasicOperations:

    def test_first_step_easy(self):
        test1 = Basic_methods(params.arr1.copy())
        mat1, H1 = test1.first_step()
        assert params.equal_matrix(mat1, params.res1[0])
        assert H1 == params.res1[1]

        test2 = Basic_methods(params.arr2.copy())
        mat2, H2 = test2.first_step()
        assert params.equal_matrix(mat2, params.res2[0])
        assert H2 == params.res2[1]