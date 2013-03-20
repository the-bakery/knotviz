
class Polymorpher(object):

    def __call__(self, *arg):
        argtype = arg[0].__class__
        while (not hasattr(self, argtype.__name__)
          and argtype != object ):
            argtype = argtype.__bases__[0]
        return getattr(self, argtype.__name__)(*arg)
