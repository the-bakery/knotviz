
from sympy import Dummy, Lambda, diff, sin, cos, pi

from VQM import Vec3, M3x3


class LambdaV(object):

    def __init__(self, v, e):
        self.vars = v
        self.expr = e


def ringCurve(r):
    t = Dummy('t')
    return LambdaV(t, Vec3(cos(2*pi*t), sin(2*pi*t), 0).scale(r))


def normalPatch(patch):
    (t, u) = patch.vars
    f = patch.expr
    dfdt = f.diff(t).unit()
    dfdu = f.diff(u).unit()
    return LambdaV( (t,u), dfdt.cross(dfdu) )


def tubularPatch(path, mask):
    t = path.vars
    u = mask.vars
    d0 = path.expr
    d1 = d0.diff(t).unit()
    d2 = d1.diff(t).unit()
    i = d2
    k = d1
    j = k.cross(i)
    frame = M3x3(i, j, k)
    return LambdaV( (t,u), d0 + frame.apply(mask.expr) )
