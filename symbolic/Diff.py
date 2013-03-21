
from symbolic.Expr import *
from symbolic.Polymorpher import *
from symbolic.Tree import *

from symbolic.output.SX import *


def diff(expr, var):
    return foldTree( _Diff(var), expr )


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
        return Mul( expr, Add( Mul(df, Div(g, f)), Mul(dg, Log(f)) ) )

    def Sin(self, expr, *subx):
        (f,) = expr
        (df,) = subx
        return Mul( Cos(f), df )

    def Cos(self, expr, *subx):
        (f,) = expr
        (df,) = subx
        return Mul( Neg(Sin(f)), df )

    def Exp(self, expr, *subx):
        (f,) = expr
        (df,) = subx
        return Mul( Exp(f), df )

    def Log(self, expr, *subx):
        (f,) = expr
        (df,) = subx
        return Mul( Neg(Inv(f)), df )
