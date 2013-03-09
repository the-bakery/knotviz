
from symbolic.Expr import *
from symbolic.Polymorpher import *


def checkKind(expr):
    return inferKind != Unknown


def inferKind(expr):
    return KindInference()(expr)


class KindInference(Polymorpher):

    def Expr(self, expr, *subx):
        return expr.kind

    def Add(self, expr, *subx):
        lookup = {(Unknown, Unknown): Unknown,
                  (Unknown, Scalar): Unknown,
                  (Unknown, Vector): Unknown,
                  (Scalar, Unknown): Unknown,
                  (Scalar, Scalar): Scalar,
                  (Scalar, Vector): Unknown,
                  (Vector, Unknown): Unknown,
                  (Vector, Scalar): Unknown,
                  (Vector, Vector): Vector}
        print '[%s]' % str(subx)
        expr.kind = lookup[subx]
        return expr.kind

    def Sub(self, expr, *subx):
        return self.Add(expr, *subx)

    def Neg(self, expr, *subx):
        lookup = {(Unknown,): Unknown,
                  (Scalar,): Scalar,
                  (Vector,): Vector}
        expr.kind = lookup[subx]
        return expr.kind

    def Mul(self, expr, *subx):
        lookup = {(Unknown, Unknown): Unknown,
                  (Unknown, Scalar): Unknown,
                  (Unknown, Vector): Unknown,
                  (Scalar, Unknown): Unknown,
                  (Scalar, Scalar): Scalar,
                  (Scalar, Vector): Vector,
                  (Vector, Unknown): Unknown,
                  (Vector, Scalar): Vector,
                  (Vector, Vector): Unknown}
        expr.kind = lookup[subx]
        return expr.kind

    def Div(self, expr, *subx):
        lookup = {(Unknown, Unknown): Unknown,
                  (Unknown, Scalar): Unknown,
                  (Unknown, Vector): Unknown,
                  (Scalar, Unknown): Unknown,
                  (Scalar, Scalar): Scalar,
                  (Scalar, Vector): Unknown,
                  (Vector, Unknown): Unknown,
                  (Vector, Scalar): Vector,
                  (Vector, Vector): Unknown}
        expr.kind = lookup[subx]
        return expr.kind

    def Inv(self, expr, *subx):
        lookup = {(Unknown,): Unknown,
                  (Scalar,): Scalar,
                  (Vector,): Unknown}
        expr.kind = lookup[subx]
        return expr.kind

    def Pow(self, expr, *subx):
        (b, e) = subx
        if b.kind == Scalar and e.kind == Scalar:
            expr.kind = Scalar
        else:
            expr.kind = Unknown
        return expr.kind
