class Vec2D(tuple):

    def __new__(klass, x=0, y=0):
        if type(x) == tuple:
            y = x[1]
            x = x[0]
        return tuple.__new__(klass, (x, y))

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, other):
        if type(other) is Vec2D:
            return (approx_equal(self.x, other.x, 0.1) and
                    approx_equal(self.y, other.y, 0.1))
        else:
            return False

    def __getattr__(self, attr):
        if attr == 'x' or attr == 'width':
            return self[0]
        elif attr == 'y' or attr == 'height':
            return self[1]
        else:
            raise AttributeError

    def __neg__(self):
        return Vec2D(-self.x, -self.y)

    def __add__(self, other):
        if issubclass(type(other), tuple):
            return Vec2D(self.x + other[0], self.y + other[1])
        elif type(other) == int or type(other) == float:
            return Vec2D(self.x + other, self.y + other)
        else:
            raise TypeError

    def __radd__(self, other):
        if issubclass(type(other), tuple):
            return Vec2D(self.x + other[0], self.y + other[1])
        elif type(other) == int or type(other) == float:
            return Vec2D(self.x + other, self.y + other)
        else:
            raise TypeError

    def __sub__(self, other):
        if issubclass(type(other), tuple):
            return Vec2D(self.x - other[0], self.y - other[1])
        elif type(other) == int or type(other) == float:
            return Vec2D(self.x - other, self.y - other)
        else:
            raise TypeError

    def __rsub__(self, other):
        if issubclass(type(other), tuple):
            return Vec2D(self.x - other[0], self.y - other[1])
        elif type(other) == int or type(other) == float:
            return Vec2D(self.x - other, self.y - other)
        else:
            raise TypeError

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Vec2D(self.x * other, self.y * other)
        else:
            raise TypeError

    def __rmul__(self, other):
        if type(other) == int or type(other) == float:
            return Vec2D(self.x * other, self.y * other)
        else:
            raise TypeError


def approx_equal(a, b, epsilon):
    return abs(a - b) < epsilon
