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

    def Float(self, expr):
        #TODO: check precision
        return str(expr)

    def Rational(self, expr):
        return self.paren( str(expr.p) + '/' + str(expr.q) )

    def Symbol(self, expr):
        return str(expr)

    def Add(self, expr):
        return self.paren( ' + '.join(glsl(e) for e in expr.args) )

    def Mul(self, expr):
        return self.paren( ' * '.join(glsl(e) for e in expr.args) )

    def Pow(self, expr):
        return 'pow' + self.paren( ', '.join(self(expr.args[0]), self(expr.args[1])) )

    def paren(self, text):
        return '(' + text + ')'

    def __call__(self, expr):
        expr = sympify(expr)
        try:
            func = getattr(self, type(expr).__name__)
            return func(expr)
        except Exception as e:
            return '/*' + str(e) + '*/'

glsl = GLSL()
