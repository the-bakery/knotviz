
from symbolic.Expr import *
from symbolic.Diff import *
from symbolic.output.GLSL import *


def ringCurve(r=1.0):
    t = Dummy()
    tau = Floating(2 * 3.1415926)
    return LambdaV( (t,), Vec3(cos(tau*t), sin(tau*t), 0).scale(r) )


def normalPatch(patch):
    (t, u) = patch.vars
    f = patch.expr
    dfdt = diff(f, t)
    dfdu = diff(f, t)
    expr = normalize( cross(dfdt, dfdu) )
    return Function( (t,u), expr )


def tubularPatch(path, mask):
    (t,) = path.vars
    (u,) = mask.vars
    d0 = path.expr
    d1 = normalize( diff(d0, t) )
    d2 = normalize( diff(d1, t) )
    i = d2
    k = d1
    j = cross(k, i)
    print 'i: %s' % i
    print 'j: %s' % j
    print 'k: %s' % k
    frame = M3x3(i, j, k)
    expr = d0 + frame(mask.expr)
    return Function( (t,u), expr )


def torusPatch(r_maj=2.0, r_min=1.0):
    surf = tubularPatch(ringCurve(r_maj), ringCurve(r_min))
    return surf


def torusKnot(p, q):
    torus = torusPatch()
    (t, u) = torus.vars
    expr = torus.expr.fmap( lambda e: e.subs( [(t, p*t), (u, q*t)] ) )
    return LambdaV( (t,), expr.fmap(simplify) )

surf = tubularPatch( torusKnot(2,3), ringCurve() )

normal = normalPatch( torusPatch() )

if __name__=='__main__':
   print normal.expr
   print compileFunction('normal', normal)
