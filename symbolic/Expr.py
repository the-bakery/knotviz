
from __future__ import division

from symbolic.Tree import *


Unknown = 0
Scalar = 1
Vector = 2


class Expr(Tree):

    def __init__(self, *subx):
        super(Expr, self).__init__(*subx)
        self.kind = Unknown

    def __add__(self, expr):
        return Add(self, expr)

    def __neg__(self):
        return Neg(self)

    def __sub__(self, expr):
        return Sub(self, expr)

    def __mul__(self, expr):
        return Mul(self, expr)

    def __truediv__(self, expr):
        return Div(self, expr)

    def __pow__(self, expr):
        return Pow(self, expr)


def dot(a, b):
    return Dot(a, b)


def cross(a, b):
    return Cross(a, b)


class Atom(Expr):

    def __init__(self, kind):
        super(Atom, self).__init__()
        self.kind = kind


class Symbol(Atom):

    def __init__(self, kind, name):
        """For kind-checking to work, the kind of every leaf node
        in the tree must be given."""
        super(Symbol, self).__init__(kind)
        self.name = name


class Dummy(Symbol):

    count = 0

    def __init__(self, kind):
        super(Dummy, self).__init__(kind, '_%s' % count)
        count += 1


class Constant(Atom):

    def __init__(self, kind, value):
        super(Constant, self).__init__(kind)
        self.value = value


class Integer(Constant):

    def __init__(self, value):
        super(Integer, self).__init__(Scalar, value)


class Floating(Constant):

    def __init__(self, value):
        super(Floating, self).__init__(Scalar, value)


class Null(Constant):

    def __init__(self):
        super(Null, self).__init__(Vector, 0)


class Compound(Expr):

    def __init__(self, *args):
        super(Compound, self).__init__(*args)


class Vec3(Compound):

    def __init__(self, x, y, z):
        super(Vec3, self).__init__(x, y, z)
        self.kind = Vector


class Add(Compound):

    def __init__(self, x, y):
        super(Add, self).__init__(x, y)


class Neg(Compound):

    def __init__(self, x):
        super(Neg, self).__init__(x)


class Sub(Compound):

    def __init__(self, x, y):
        super(Sub, self).__init__(x, y)


class Mul(Compound):

    def __init__(self, x, y):
        super(Mul, self).__init__(x, y)


class Dot(Compound):

    def __init__(self, x, y):
        super(Dot, self).__init__(x, y)
        self.kind = Scalar


class Cross(Compound):

    def __init__(self, x, y):
        super(Cross, self).__init__(x, y)
        self.kind = Vector


class Inv(Compound):

    def __init__(self, x):
        super(Inv, self).__init__(x)


class Pow(Compound):

    def __init__(self, b, e):
        super(Pow, self).__init__(b, e)


class Root(Compound):

    def __init__(self, b, e):
        super(Root, self).__init__(b, e)


class Div(Compound):

    def __init__(self, x, y):
        super(Div, self).__init__(x, y)
