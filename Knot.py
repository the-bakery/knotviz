
import sympy
from sympy import Dummy, sin, cos
from sympy import simplify, trigsimp

from VQM import *
from GLSL import *

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
    dfdt = diff(f,t)
    dfdu = diff(f,u)
    expr = dfdt.cross(dfdu).unit()
    return LambdaV( (t,u), expr.fmap(simplify) )


def tubularPatch(path, mask):
    (t,) = path.vars
    (u,) = mask.vars
    d0 = path.expr
    d1 = diff(d0,t).unit().fmap(simplify)
    d2 = diff(d1,t).unit().fmap(simplify)
    i = d2
    k = d1
    j = k.cross(i).fmap(simplify)
    print 'i: %s' % i
    print 'j: %s' % j
    print 'k: %s' % k
    frame = M3x3(i, j, k)
    expr = d0 + frame(mask.expr)
    return LambdaV( (t,u), expr.fmap(simplify) )


def torusPatch(r_maj=2.0, r_min=1.0):
    surf = tubularPatch(ringCurve(r_maj), ringCurve(r_min))
    surf.expr.fmap(simplify)
    return surf


def torusKnot(p, q):
    torus = torusPatch()
    (t, u) = torus.vars
    expr = torus.expr.fmap( lambda e: e.subs( [(t, p*t), (u, q*t)] ) )
    return LambdaV( (t,), expr.fmap(simplify) )

# surf = tubularPatch( torusKnot(2,3), ringCurve() )

normal = normalPatch( torusPatch() )

if __name__=='__main__':
   print normal.expr
   print compileFunction('normal', normal)
