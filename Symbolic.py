
from __future__ import division
from collections import Iterable
from IPython.display import Latex, display


Scalar = 0
Vector = 1

kindsymbol = {Scalar: 'S', Vector: 'V'}


class Translator(object):

    def __call__(self, expr):
        try:
            func = getattr(self, type(expr).__name__)
            return func(expr)
        except Exception as e:
            return self.__default__(expr)


class SX(Translator):

    def Integer(self, expr):
        return str(expr[0])

    def Symbol(self, expr):
        return expr[0]

    def __default__(self, expr):
        return '(%s %s)' % (expr.name(), ' '.join(self(c) for c in expr))

toSX = SX()


class LaTeX(Translator):

    def Constant(self, expr):
        if expr.kind == Vector:
            form = '\\vec{%s}'
        else:
            form = '%s'
        return form % str(expr[0])

    def Integer(self, expr):
        return str(expr[0])

    def Null(self, expr):
        return '\\vec{0}'

    def Symbol(self, expr):
        if expr.kind == Vector:
            form = '\\vec{%s}'
        else:
            form = '%s'
        return form % expr[0]

    def Add(self, expr):
        return '%s + %s' % tuple(self(c) for c in expr)

    def Sub(self, expr):
        return '%s - %s' % tuple(self(c) for c in expr)

    def Mul(self, expr):
        if (expr[0].kind, expr[1].kind) == (Vector, Vector):
            form = '\\left\\langle %s, %s \\right\\rangle'
        else:
            form = '%s \\cdot %s'
        return form % tuple(self(c) for c in expr)

    def Div(self, expr):
        return '\\frac{%s}{%s}' % tuple(self(c) for c in expr)

    def Pow(self, expr):
        return '%s^{%s}' % tuple(self(c) for c in expr)

    def __default__(self, expr):
        return '/* %s */' % expr.name()


def toLaTeX(expr):
    return display( Latex( '$$ %s $$' % LaTeX()(expr) ) )


class Expr(object):

    def __init__(self, kind, *args):
        self.kind = kind
        self.args = args

    def __iter__(self):
        return self.args.__iter__()

    def name(self):
        return type(self).__name__

    def __getitem__(self, index):
        return self.args[index]

    def __repr__(self):
        return '%s%s(%s)' % ( kindsymbol[self.kind],
                              type(self).__name__,
                              ', '.join(str(c) for c in self) )

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


def countOps(expr):
    if isinstance(expr, Atom):
        return 0
    return 1 + sum( countOps(x) for x in expr )


def dot(a, b):
    return Dot(a, b)


def cross(a, b):
    return Cross(a, b)


class Atom(Expr):

    def __init__(self, kind, *args):
        super(Atom, self).__init__(kind, *args)


class Constant(Atom):

    def __init__(self, kind, *args):
        super(Constant, self).__init__(kind, *args)

    def diff(self, var):
        assert var.kind == Scalar
        return Constant(self.kind, 0)


class Integer(Constant):

    def __init__(self, val):
        super(Integer, self).__init__(Scalar, val)

    def __int__(self):
        return self.args[0]


class Floating(Constant):

    def __init__(self, val):
        super(Floating, self).__init__(Scalar, val)

    def __float__(self):
        return float(self.args[0])


class Null(Constant):

    def __init__(self):
        super(Null, self).__init__(Vector, 0)


class Symbol(Atom):

    def __init__(self, kind, name):
        super(Symbol, self).__init__(kind, name)

    def diff(self, var):
        assert var.kind == Scalar
        assert isinstance(var, Symbol)
        if self.kind == Scalar:
            if var.args[0] == self.args[0]:
                return Integer(1)
            else:
                return Integer(0)
        else:
            return Null()


class Compound(Expr):

    def __init__(self, kind, *args):
        super(Compound, self).__init__(kind, *args)


class Vec3(Compound):

    def __init__(self, x, y, z):
        super(Vec3, self).__init__(Vector, x, y, z)

    def diff(self, var):
        assert var.kind == Scalar
        return Vec3(*(c.diff(var) for c in self))


class Add(Compound):

    def __init__(self, x, y):
        assert x.kind == y.kind
        super(Add, self).__init__(x.kind, x, y)

    def diff(self, var):
        assert var.kind == Scalar
        for t in self:
            print t
        return Add(*(t.diff(var) for t in self))


class Neg(Compound):

    def __init__(self, x):
        super(Neg, self).__init__(x.kind, x)

    def diff(self, var):
        return Neg(*(c.diff(var) for c in self))


class Sub(Compound):

    def __init__(self, x, y):
        assert x.kind == y.kind
        super(Sub, self).__init__(x.kind, x, y)

    def diff(self, var):
        assert var.kind == Scalar
        return Sub(*(t.diff(var) for t in self))


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

    def diff(self, var):
        assert var.kind == Scalar
        (x, y) = self
        return Add( Mul(x.diff(var), y), Mul(x, y.diff(var)) )


class Dot(Compound):

    def __init__(self, x, y):
        assert x.kind == Vector and y.kind == Vector
        super(Dot, self).__init__(Scalar, x, y)

    def diff(self, var):
        assert var.kind == Scalar
        (x, y) = self
        return Add( Dot(x.diff(var), y), Dot(x, y.diff(var)) )


class Cross(Compound):

    def __init__(self, x, y):
        assert x.kind == Vector and y.kind == Vector
        super(Cross, self).__init__(Vector, x, y)

    def diff(self, var):
        assert var.kind == Scalar
        (x, y) = self
        return Add( Cross(x.diff(var), y), Cross(x, y.diff(var)) )


class Inv(Compound):

    def __init__(self, x):
        super(Inv, self).__init__(x.kind, x)

    def diff(self, var):
        assert var.kind == Scalar
        return Neg( Div( c.diff(var), Pow(c, Integer(2)) ) for c in self )


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

    def diff(self, var):
        assert var.kind == Scalar
        (b, e) = self
        e_minus_1 = Sub( e, Integer(1) )
        return Mul( e, Pow(b, e_minus_1) )


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

    def diff(self, var):
        assert var.kind == Scalar
        (x, y) = self
        numerator = Sub( Mul(x.diff(var), y), Mul(x, y.diff(var)) )
        denominator = Pow( y, Integer(2) )
        return Div(numerator, denominator)


def match(pattern, structure, bindings=None):

    if bindings == None:
        bindings = {}

    if isinstance(pattern, Symbol):
        if pattern.args[0] in bindings:
            if bindings[pattern.args[0]] == structure:
                return bindings
            else:
                return False
        else:
            bindings[pattern.args[0]] = structure
            return bindings

    if pattern.__class__ != structure.__class__:
        return False

    if not isinstance(pattern, Iterable) or not isinstance(structure, Iterable):
        if pattern == structure:
            return bindings
        else:
            return False

    subp = list(pattern)
    subs = list(structure)

    if len(subp) != len(subs):
        return False

    for p, s in zip(subp, subs):
        if match(p, s, bindings) == False:
            return False

    return bindings
