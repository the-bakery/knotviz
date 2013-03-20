
from symbolic.Expr import *
from symbolic.Polymorpher import *
from symbolic.Tree import *

from symbolic.output.SX import *


def diff(var, tree):
    return foldTree( _Diff(var), tree )


class _Diff(Polymorpher):

    def __init__(self, var):
        self.var = var

    def Constant(self, expr):
        if expr.kind == Scalar:
            return Integer(0)
        else:
            return Null

    def Symbol(self, expr):
        if expr == self.var:
            return Integer(1)
        else:
            return Integer(0)

    def Vec3(self, expr, *subx):
        return Vec3(*subx)

    def Add(self, expr, *subx):
        return Add(*subx)

    def Sub(self, expr, *subx):
        return Sub(*subx)

    def Neg(self, expr, *subx):
        return Neg(*subx)

    def Mul(self, expr, *subx):
        print toSX(expr)
        (f, g) = expr
        (df, dg) = subx
        return Add( Mul(df, g), Mul(f, dg) )

    def Dot(self, expr, *subx):
        (f, g) = expr
        (df, dg) = subx
        return Add( Dot(df, g), Dot(f, dg) )

    def Cross(self, expr, *subx):
        (f, g) = expr
        (df, dg) = subx
        return Add( Cross(df, g), Cross(f, dg) )

    def Inv(self, expr, *subx):
        (g,) = expr
        (dg,) = subx
        return Div( Neg(dg), Pow( g, Integer(2) ) )

    def Div(self, expr, *subx):
        (f, g) = expr
        (df, dg) = subx
        return Div( Sub( Mul(df, g), Mul(f, dg) ), Pow( g, Integer(2) ) )

    def Pow(self, expr, *subx):
        (f, g) = expr
        (df, dg) = subx
        return Mul( g, Pow( df, Sub(g, Integer(1)) ) )
