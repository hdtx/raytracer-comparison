import math

class Vec3:
    def __init__(self, comp):
        self.comp = tuple(comp)

    def __repr__(self) -> str:
        return str(self.comp)

    def x(self):
        return self.comp[0]

    def y(self):
        return self.comp[1]
        
    def z(self):
        return self.comp[2]
        
    def verif_type(other, op_name):
        if type(other) is not Vec3:
            raise NotImplementedError(
                'cannot {} Vec3 and {}'.format(op_name, type(other)))

    def __eq__(self, other):
        Vec3.verif_type(other, 'eq')
        return self.comp == other.comp

    def __add__(self, other):
        Vec3.verif_type(other, 'add')
        return Vec3(v + other.comp[i] for i, v in enumerate(self.comp))

    def __neg__(self):
        return Vec3(-v for v in self.comp)

    def __sub__(self, other):
        Vec3.verif_type(other, 'sub')
        return Vec3(v - other.comp[i] for i, v in enumerate(self.comp))

    def __mul__(self, other):
        if type(other) is not int and type(other) is not float:
            raise NotImplementedError(
                'cannot mul Vec3 and {}'.format(type(other)))
        return Vec3(v * other for v in self.comp)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) is not int and type(other) is not float:
            raise NotImplementedError(
                'cannot div Vec3 and {}'.format(type(other)))
        return Vec3(v / other for v in self.comp)

    def dot(self, other):
        Vec3.verif_type(other, 'dot')
        return sum(v * other.comp[i] for i, v in enumerate(self.comp))

    def cross(self, other):
        Vec3.verif_type(other, 'cross')
        ax, ay, az = self.comp
        bx, by, bz = other.comp
        return Vec3((ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx))

    def norm(self):
        return math.sqrt(self.dot(self))

    def unity(self):
        return self / self.norm()

    def compare(self, other, tol):
        Vec3.verif_type(other, 'compare')
        return (self - other).norm() < abs(tol)

    def at_len(self, t):
        if type(t) is not int and type(t) is not float:
            raise NotImplementedError(
                'cannot at_len with {}'.format(type(t)))
        return self.unity() * t

    def abs(self):
        return Vec3(abs(x) for x in self.comp)
