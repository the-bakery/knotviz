
from __future__ import division

from symbolic.Tree import *


Scalar = 0
Vector = 1


class Expr(Tree):

    def __init__(self, kind, *subx):
        super(Expr, self).__init__(*subx)
        self.kind = kind

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
        super(Atom, self).__init__(kind)


class Symbol(Atom):

    def __init__(self, kind, name):
        super(Symbol, self).__init__(kind)
        self.name = name


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

    def __init__(self, kind, *args):
        super(Compound, self).__init__(kind, *args)


class Vec3(Compound):

    def __init__(self, x, y, z):
        super(Vec3, self).__init__(Vector, x, y, z)


class Add(Compound):

    def __init__(self, x, y):
        assert x.kind == y.kind
        super(Add, self).__init__(x.kind, x, y)


class Neg(Compound):

    def __init__(self, x):
        super(Neg, self).__init__(x.kind, x)


class Sub(Compound):

    def __init__(self, x, y):
        assert x.kind == y.kind
        super(Sub, self).__init__(x.kind, x, y)


class Mul(Compound):

    def __init__(self, x, y):
        if x.kind == Scalar:
            kind = y.kind
        else:
            if y.kind == Scalar:
                kind = Vector
            else:
                kind = Scalar
        super(Mul, self).__init__(kind, x, y)


class Dot(Compound):

    def __init__(self, x, y):
        assert x.kind == Vector and y.kind == Vector
        super(Dot, self).__init__(Scalar, x, y)


class Cross(Compound):

    def __init__(self, x, y):
        assert x.kind == Vector and y.kind == Vector
        super(Cross, self).__init__(Vector, x, y)


class Inv(Compound):

    def __init__(self, x):
        super(Inv, self).__init__(x.kind, x)


class Pow(Compound):

    def __init__(self, b, e):
        if b.kind == Vector:
            assert isinstance(e, Integer)
            if int(e) % 2 == 0:
                kind = Scalar
            else:
                kind = Vector
        else:
            kind = Scalar
        super(Pow, self).__init__(kind, b, e)


class Div(Compound):

    def __init__(self, x, y):
        if x.kind == Scalar:
            kind = y.kind
        else:
            if y.kind == Scalar:
                kind = Vector
            else:
                kind = Scalar
        super(Div, self).__init__(kind, x, y)