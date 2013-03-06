
from symbolic.Expr import *
from symbolic.Polymorpher import *
from symbolic.Tree import *


def toSX(tree):
    return foldTree( _SX(), tree )


class _SX(Polymorpher):

    def Integer(self, expr):
        return str(expr.value)

    def Symbol(self, expr):
        return expr.name

    def Compound(self, expr, *subx):
        return '(%s %s)' % (expr.name(), ' '.join(subx))
