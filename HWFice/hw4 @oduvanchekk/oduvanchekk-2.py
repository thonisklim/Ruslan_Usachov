class Vector:
    def __init__(self, coords):
        self.coords = coords

    def __str__(self):
        return '(' + ','.join([str(i) for i in self.coords]) + ')'

    def add(self, vector):
        return Vector([self.coords[i] + vector.coords[i] for i in range(len(self.coords))])

    def subtract(self, vector):
        return Vector([self.coords[i] - vector.coords[i] for i in range(len(self.coords))])

    def dot(self, vector):
        return sum([self.coords[i] * vector.coords[i] for i in range(len(self.coords))])

    def norm(self):
        return sum([self.coords[i] ** 2 for i in range(len(self.coords))]) ** 0.5

    def equals(self, vector):
        return self.coords == vector.coords


