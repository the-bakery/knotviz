import VQM
from sympy import Symbol, Dummy, pi, sin, cos, sympify
from sympy.core import Atom


class Uniform(Dummy):
    def __init__(self, *args):
        super(Uniform, self).__init__(*args)


class Varying(Dummy):
    def __init__(self, *args):
        super(Varying, self).__init__(*args)


class GLSL(object):

    def Integer(self, expr):
        return str(expr)

    def int(self, expr):
        return str(expr)

    def Float(self, expr):
        #TODO: check precision
        return str(expr)

    def Rational(self, expr):
        return self.paren( self(expr.p) + '/' + self(expr.q) )

    def Symbol(self, expr):
        return str(expr)
    
    def Dummy(self, expr):
        return 'v%s' % expr.name

    def Varying(self, expr):
        return self.Dummy(expr)

    def Uniform(self, expr):
        return self.Dummy(expr)
    
    def Add(self, expr):
        return self.paren( ' + '.join(glsl(e) for e in expr.args) )

    def Mul(self, expr):
        return self.paren( ' * '.join(glsl(e) for e in expr.args) )

    def Pow(self, expr):
        return 'pow' + self.paren( ', '.join((self(expr.args[0]), self(expr.args[1]))) )

    def Vec3(self, expr):
        return 'vec4(%s, %s, %s, 1.0)' % (glsl(expr.x), glsl(expr.y), glsl(expr.z))

    def sin(self, expr):
        return 'sin(%s)' % glsl(expr.args[0])

    def cos(self, expr):
        return 'cos(%s)' % glsl(expr.args[0])

    def NegativeOne(self, expr):
        return '-1'
    
    def paren(self, text):
        return '(' + text + ')'

    def __call__(self, expr):
        # expr = sympify(expr)
        try:
            func = getattr(self, type(expr).__name__)
            return func(expr)
        except Exception as e:
            return '/* %s, %s */' % (e, expr)

glsl = GLSL()


def compileFunction(name, func):
    args = ', '.join( 'float ' + glsl(var) for var in func.vars)
    print [ var.name for var in func.vars ]
    body = glsl(func.expr)
    return 'vec4 %s(%s) { return %s; }' % (name, args, body)

