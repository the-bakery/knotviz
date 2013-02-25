
import sympy
from sympy import Dummy, Lambda, sin, cos
from sympy import simplify, trigsimp
from sympy.physics.mechanics import *

from VQM import *
from GLSL import *

Frame = ReferenceFrame('Frame')


class LambdaV(object):
    def __init__(self, v, e):
        self.vars = v
        self.expr = e


def diff(fun, var):
    return fun.diff(var, Frame)


def ringCurve(r=1.0):
    t = Dummy()
    pi = Symbol('pi')
    expr = r*cos(2*pi*t)*Frame.x + r*sin(2*pi*t)*Frame.y
    return LambdaV( (t,), expr )


def normalPatch(patch):
    (t, u) = patch.vars
    f = patch.expr
    dfdt = diff(f,t)
    dfdu = diff(f,u)
    expr = dfdt.cross(dfdu).normalize()
    # expr.simplify()
    return LambdaV( (t,u), expr )


def tubularPatch(path, mask):
    (t,) = path.vars
    (u,) = mask.vars
    d0 = path.expr
    d1 = diff(d0,t).normalize()
    d2 = diff(d1,t).normalize()
    i = d2
    k = d1
    j = k.cross(i)
    i.simplify()
    k.simplify()
    j.simplify()
    print 'i: %s' % i
    print 'j: %s' % j
    print 'k: %s' % k
    # frame = M3x3(i, j, k)
    # expr = d0 + i*dot(Frame.x, mask.expr) +  #frame(mask.expr)
    expr = (d0 +
            i*dot(Frame.x, mask.expr) +
            j*dot(Frame.y, mask.expr) +
            k*dot(Frame.z, mask.expr))
    # expr.simplify()
    return LambdaV( (t,u), expr )


def torusPatch(r_maj=2.0, r_min=1.0):
    surf = tubularPatch(ringCurve(r_maj), ringCurve(r_min))
    surf.expr.simplify()
    return surf


def torusKnot(p, q):
    torus = torusPatch()
    (t, u) = torus.vars
    expr = torus.expr.subs( [(t, p*t), (u, q*t)] )
    # expr.simplify()
    return LambdaV( (t,), expr )

surf = tubularPatch( torusKnot(2,3), ringCurve() )

# normal = normalPatch( torusPatch() )

if __name__=='__main__':
   surf.expr.simplify()
   print surf.expr
   print compileFunction('surf', surf)
