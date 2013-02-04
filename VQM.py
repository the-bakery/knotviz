
from __future__ import division

from sympy import diff, sqrt


class Vec3(object):

    def __init__(self, *xyz):
        print xyz
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __repr__(self):
        return "Vec3(%s)" % (", ".join(str(x) for x in self))

    def fmap(self, f):
        return Vec3(*(f(x) for x in self))

    def diff(self, *d):
        return self.fmap(lambda f: diff(f, *d))

    def scale(self, f):
        return Vec3(f*self.x, f*self.y, f*self.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def cross(self, v):
        return Vec3(self.y*v.z - self.z*v.y,
                    self.z*v.x - self.x*v.z,
                    self.x*v.y - self.y*v.x)

    def dot(self, v):
        return self.x*v.x + self.y*v.y + self.z*v.z

    def norm(self):
        return sqrt(self.dot(self))

    def unit(self):
        return self.scale(1 / self.norm())

    def __add__(self, v):
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)


class Quat(object):

    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def scale(self, f):
        return Quat(f*self.w, f*self.x, f*self.y, f*self.z)

    def __neg__(self):
        return Quat(-self.w, -self.x, -self.y, -self.z)

    def conj(self):
        return Quat(w, -x, -y, -z)

    def dot(self, q):
        return self.w*q.w + self.x*q.x + self.y*q.y + self.z*q.z

    def unit(self):
        return self.scale(1 / self.norm())

    def norm(self):
        return sqrt(self.dot(self))

    def __add__(self, q):
        return Quat(self.w + q.w, self.x + q.x, self.y + v.y, self.z + v.z)

    def __sub__(self, q):
        return Quat(self.w - q.w, self.x - q.x, self.y - v.y, self.z - v.z)

    def __mul__(self, q):
	return Quat(self.w*q.w - self.x*q.x - self.y*q.y - self.z*q.z,
                    self.w*q.x + self.x*q.w + self.y*q.z - self.z*q.y,
                    self.w*q.y - self.x*q.z + self.y*q.w + self.z*q.x,
                    self.w*q.z + self.x*q.y - self.y*q.x + self.z*q.w)

    def __truediv__(self, q):
        return self * q.conj().unit()

    def matrix(self):
	return M3x3(Vec3(w*w+x*x-y*y-z*z, 2 * (x*y + w*z), 2 * (x*z - w*y)),
		    Vec3(2 * (x*y - w*z), w*w-x*x+y*y-z*z, 2 * (y*z + w*x)),
		    Vec3(2 * (x*z + w*y), 2 * (y*z - w*x), w*w-x*x-y*y+z*z))


class M3x3(object):

    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def scale(self, f):
        return M3x3(self.X.scale(f), self.Y.scale(f), self.Z.scale(f))

    def __neg__(self):
        return M3x3(-self.X, -self.Y, -self.Z)

    def __add__(self, m):
        return M3x3(self.X + m.X, self.Y + m.Y, self.Z + m.Z)

    def __sub__(self, m):
        return M3x3(self.X - m.X, self.Y - m.Y, self.Z - m.Z)

    def apply(self, v):
        return self.X.scale(v.x) + self.Y.scale(v.y) + self.Z.scale(v.z)

    def __mul__(self, m):
        return M3x3(self.apply(m.X), self.apply(m.Y), self.apply(m.Z))
