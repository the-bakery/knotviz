
import sympy
from sympy import Dummy, sin, cos, trigsimp

from VQM import Vec3, Quat, M3x3


def diff(v, d):
    if isinstance(v, Vec3):
        return v.fmap(lambda e: sympy.diff(e, d))
    else:
        return sympy.diff(v, d)


class LambdaV(object):

    def __init__(self, v, e):
        self.vars = v
        self.expr = e


def ringCurve(r=1.0):
    t = Dummy()
    pi = 3.1415926
    return LambdaV( (t,), Vec3(cos(2*pi*t), sin(2*pi*t), 0).scale(r) )


def normalPatch(patch):
    (t, u) = patch.vars
    f = patch.expr
    dfdt = diff(f,t).unit()
    dfdu = diff(f,u).unit()
    return LambdaV( (t,u), dfdt.cross(dfdu) )


def tubularPatch(path, mask):
    (t,) = path.vars
    (u,) = mask.vars
    d0 = path.expr
    d1 = diff(d0,t).unit()
    d2 = diff(d1,t).unit()
    i = d2
    k = d1
    j = k.cross(i)
    frame = M3x3(i, j, k)
    return LambdaV( (t,u), d0 + frame(mask.expr) )


def torusPatch(r_maj=2.0, r_min=1.0):
    return tubularPatch(ringCurve(r_maj), ringCurve(r_min))


torus = torusPatch()
torus.expr = torus.expr.fmap(trigsimp)
