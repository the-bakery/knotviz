
from symbolic.Expr import *
from symbolic.Polymorpher import *
from symbolic.Tree import *


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
