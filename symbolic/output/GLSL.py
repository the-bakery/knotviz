
from symbolic.Expr import *
from symbolic.Polymorpher import *
from symbolic.Tree import *
from symbolic.KindCheck import *


class Uniform(Dummy):
    def __init__(self, *args):
        super(Uniform, self).__init__(*args)


class Varying(Dummy):
    def __init__(self, *args):
        super(Varying, self).__init__(*args)


def glsl(name, func):
    assert checkKind(func)
    rtyp = func.expr.kind == Scalar ? 'float' : 'vec3';
    args = ', '.join('float %s' % sym for sym in func.syms)
    body = toGLSL(expr)
    return '%s %s(%s) { return %s; }' % (rtyp, name, args, body)


def toGLSL(tree):
    return foldTree( _GLSL(), tree )


class _GLSL(Polymorpher):

    def Constant(self, expr):
        if expr.kind == Scalar:
            return str(expr.value)
        else:
            return 'vec3(0,0,0)'

    def Symbol(self, expr):
        return expr.name

    def Vec3(self, expr, *subx):
        return 'vec3(%s,%s,%s)' % subx

    def Add(self, expr, *subx):
        return '(%s + %s)' % subx

    def Sub(self, expr, *subx):
        return '(%s - %s)' % subx

    def Neg(self, expr, *subx):
        return '(-%s)' % subx

    def Mul(self, expr, *subx):
        return '(%s * %s)' % subx

    def Dot(self, expr, *subx):
        return 'dot(%s, %s)' % subx

    def Cross(self, expr, *subx):
        return 'cross(%s, %s)' % subx

    def Inv(self, expr, *subx):
        return '(1.0 / %s)' % subx

    def Div(self, expr, *subx):
        return '(%s / %s)' % subx

    def Pow(self, expr, *subx):
        return 'pow(%s, %s)' % subx

    def Sin(self, expr, *subx):
        return 'sin(%s)' % subx

    def Cos(self, expr, *subx):
        return 'cos(%s)' % subx

    def Exp(self, expr, *subx):
        return 'exp(%s)' % subx

    def Log(self, expr, *subx):
        return 'log(%s)' % subx
