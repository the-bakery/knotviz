
from IPython.display import Latex, display

from symbolic.Expr import *
from symbolic.Polymorpher import *
from symbolic.Tree import *


def toLatex(tree):
    return Latex( '$$%s$$' % foldTree( _LaTeX(), tree ) )


class _LaTeX(Polymorpher):

    def Constant(self, expr):
        if expr.kind == Scalar:
            return str(expr.value)
        else:
            return '\\vec{%s}' % str(expr.value)

    def Symbol(self, expr):
        if expr.kind == Scalar:
            return expr.name
        if expr.kind == Vector:
            return '\\vec{%s}' % expr.name

    def Vec3(self, expr, *subx):
        return ('\\left[ \\begin{array}{c}'
                '%s \\\\ %s \\\\ %s'
                '\\end{array} \\right]') % subx

    def Add(self, expr, *subx):
        return '\\left(%s + %s\\right)' % subx

    def Sub(self, expr, *subx):
        return '\\left(%s - %s\\right)' % subx

    def Neg(self, expr, *subx):
        return '-\\left(%s\\right)' % subx

    def Mul(self, expr, *subx):
        return '\\left(%s \\cdot %s\\right)' % subx

    def Dot(self, expr, *subx):
        return '\\left\\langle%s, %s\\right\\rangle' % subx

    def Cross(self, expr, *subx):
        return '\\left(%s \\times %s\\right)' % subx

    def Inv(self, expr, *subx):
        return '\\left(%s\\right)^{-1}' % subx

    def Div(self, expr, *subx):
        return '\\frac{%s}{%s}' % subx

    def Pow(self, expr, *subx):
        return '{%s}^{%s}' % subx
