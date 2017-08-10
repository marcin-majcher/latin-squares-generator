from random import randint


class LatinSquare:

    def __init__(self, size):
        self.size = size
        self.square = [[None for i in range(self.size)] for j in range(self.size)]

    def get_cell(self, point):
        return self.square[point[0]][point[1]]

    def set_cell(self, point, value):
        self.square[point[0]][point[1]] = value

    def to_incidence_cube(self):
        ic = IncidenceCube(self.size)

        for x in range(self.size):
            for y in range(self.size):
                ic.cube[x][y][self.square[x][y]] = 1

        return ic

    def is_valid(self):
        x_val = [set() for _ in range(self.size)]
        y_val = [set() for _ in range(self.size)]

        for x in range(self.size):
            for y in range(self.size):
                v = self.get_cell((x, y))
                x_val[x].add(v)
                y_val[y].add(v)

        return (all([len(x) == self.size for x in x_val]) and
                all([len(y) == self.size for y in y_val]))

    @classmethod
    def generate_default_latin_square(cls, size):
        ls = cls(size)

        for x in range(size):
            for y in range(size):
                ls.set_cell((x, y), (y + x) % size)

        return ls

    @classmethod
    def generate_latin_square(cls, size):
        latin_square = cls.generate_default_latin_square(size)
        incidence_cube = latin_square.to_incidence_cube()
        incidence_cube.shuffle(size**3)

        return incidence_cube.to_latin_square()


class IncidenceCube:

    def __init__(self, size):
        self.size = size
        self.proper = True
        self.cube = [[] for _ in range(self.size)]
        self.improper_cell = None

        for row in self.cube:
            for i in range(self.size):
                row.append([0 for _ in range(self.size)])

    def to_latin_square(self):
        ls = LatinSquare(self.size)

        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    if self.cube[x][y][z] == 1:
                        ls.set_cell((x, y), z)

        return ls

    def move(self, point_a, point_b):
        self.cube[point_a[0]][point_a[1]][point_a[2]] += 1
        self.cube[point_a[0]][point_b[1]][point_b[2]] += 1
        self.cube[point_b[0]][point_b[1]][point_a[2]] += 1
        self.cube[point_b[0]][point_a[1]][point_b[2]] += 1
        self.cube[point_a[0]][point_a[1]][point_b[2]] -= 1
        self.cube[point_a[0]][point_b[1]][point_a[2]] -= 1
        self.cube[point_b[0]][point_a[1]][point_a[2]] -= 1
        self.cube[point_b[0]][point_b[1]][point_b[2]] -= 1

    def find_cell_with_zero(self):

        while True:
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            z = randint(0, self.size - 1)

            if (self.cube[x][y][z] == 0):
                break

        return x, y, z

    def find_cell_with_one(self, x=None, y=None, z=None, skip_next=None):
        point = None

        for i in range(self.size):
            if x is None:
                cell_val = self.cube[i][y][z]
                p = (i, y, z)
            elif y is None:
                cell_val = self.cube[x][i][z]
                p = (x, i, z)
            else:
                cell_val = self.cube[x][y][i]
                p = (x, y, i)

            if cell_val == 1:
                point = p

                if not skip_next or skip_next():
                    break

        return point

    def shuffle(self, min_iterations):
        iterations = 0

        while iterations < min_iterations or not self.proper:
            iterations += 1

            if self.proper:
                point_a = self.find_cell_with_zero()
                x = self.find_cell_with_one(y=point_a[1], z=point_a[2])[0]
                y = self.find_cell_with_one(x=point_a[0], z=point_a[2])[1]
                z = self.find_cell_with_one(x=point_a[0], y=point_a[1])[2]
            else:
                skip_next = lambda: bool(randint(0, 1))
                point_a = self.improper_cell
                x = self.find_cell_with_one(y=point_a[1], z=point_a[2],
                                            skip_next=skip_next)[0]
                y = self.find_cell_with_one(x=point_a[0], z=point_a[2],
                                            skip_next=skip_next)[1]
                z = self.find_cell_with_one(x=point_a[0], y=point_a[1],
                                            skip_next=skip_next)[2]

            point_b = (x , y, z)
            self.move(point_a, point_b)
            self.proper = self.cube[point_b[0]][point_b[1]][point_b[2]] != -1

            if not self.proper:
                self.improper_cell = point_b

        return iterations
