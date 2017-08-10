import unittest
from unittest import mock

from lsquare import (
    LatinSquare,
    IncidenceCube
)


class LatinSquareTestCase(unittest.TestCase):

    def test_init_should_create_empty_square(self):
        self.assertEqual([
            [None, None, None],
            [None, None, None],
            [None, None, None]],
            LatinSquare(3).square)

    def test_get_cell(self):
        ls = LatinSquare(3)
        ls.square = [
            [1,2,3],
            [2,3,1],
            [3,1,2],
        ]

        self.assertEqual(ls.get_cell((1,2)), 1)


    def test_set_cell(self):
        ls = LatinSquare(5)
        point = (3, 4)
        val = 2
        ls.set_cell(point, val)

        self.assertEqual(ls.get_cell(point), val)

    def test_generate_default_latin_square(self):
        size = 4
        ls = LatinSquare.generate_default_latin_square(size)

        self.assertEqual(ls.size, size)
        self.assertEqual(ls.square, [
            [0, 1, 2, 3],
            [1, 2, 3, 0],
            [2, 3, 0, 1],
            [3, 0, 1, 2]
        ])

    def test_to_incidence_cube(self):
        ls = LatinSquare.generate_default_latin_square(3)
        self.assertEqual(ls.to_incidence_cube().cube, [
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
            [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
        ])

    def test_is_valid(self):
        ls = LatinSquare(4)
        ls.square = [
            [0, 1, 2, 3],
            [1, 2, 3, 0],
            [2, 3, 0, 1],
            [3, 0, 1, 2]
        ]

        self.assertTrue(ls.is_valid())

        ls.square = [
            [0, 1, 2, 3],
            [1, 2, 1, 0],
            [2, 3, 0, 1],
            [3, 0, 1, 2]
        ]

        self.assertFalse(ls.is_valid())

        ls.square = [
            [0, 1, 2, 3],
            [1, 2, 3, 0],
            [2, 3, 0, 1],
            [3, 0, 3, 2]
        ]

        self.assertFalse(ls.is_valid())


class IncidenceCubeTestCase(unittest.TestCase):

    def test_init_should_create_cube(self):
        ic = IncidenceCube(3)

        self.assertEqual(ic.cube, [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ])

    def test_to_latin_square(self):
        size = 3
        ic = IncidenceCube(size)
        ic.cube = [
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
            [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
        ]
        ls = ic.to_latin_square()

        self.assertEqual(ls.size, size)
        self.assertEqual(ls.square, [
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1]
        ])

    def test_move(self):
        ic = IncidenceCube(3)
        point_a = (0, 2, 1)
        point_b = (2, 2, 0)
        ic.move(point_a, point_b)

        self.assertEqual(ic.cube, [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ])

    @mock.patch('lsquare.randint')
    def test_find_cell_with_zero(self, mocked_randint):
        ic = IncidenceCube(3)
        point_a = (0, 1, 1)
        point_b = (2, 0, 1)
        mocked_randint.side_effect = [
            point_a[0],
            point_a[1],
            point_a[2],
            point_b[0],
            point_b[1],
            point_b[2]
        ]
        ic.cube[point_a[0]][point_a[1]][point_a[2]] = 1

        self.assertEqual(point_b, ic.find_cell_with_zero())

    def test_find_cell_with_one(self):
        point = (2, 1, 1)
        x = 1
        y = 2
        z = 0
        ic = IncidenceCube(3)
        ic.cube[x][point[1]][point[2]] = 1
        ic.cube[point[0]][y][point[2]] = 1
        ic.cube[point[0]][point[1]][z] = 1

        self.assertEqual((1, 1, 1), ic.find_cell_with_one(y=1, z=1))
        self.assertEqual((2, 2, 1), ic.find_cell_with_one(x=2, z=1))
        self.assertEqual((2, 1, 0), ic.find_cell_with_one(x=2, y=1))


if __name__ == '__main__':
    unittest.main()