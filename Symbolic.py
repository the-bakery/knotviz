
from collections import Iterable


class Symbol(object):

    def __init__(self, name):
        self.name = name


class List(object):

    def __init__(self, *args):
        self.args = iter(args)

    def __iter__(self):
        return self.args


def match(pattern, structure, bindings=None):

    if bindings == None:
        bindings = {}

    if isinstance(pattern, Symbol):
        if pattern.name in bindings:
            if bindings[pattern.name] == structure:
                return bindings
            else:
                return False
        else:
            bindings[pattern.name] = structure
            return bindings

    if pattern.__class__ != structure.__class__:
        return False

    if not isinstance(pattern, Iterable) or not isinstance(structure, Iterable):
        if pattern == structure:
            return bindings
        else:
            return False

    subp = list(pattern)
    subs = list(structure)

    if len(subp) != len(subs):
        return False

    for p, s in zip(subp, subs):
        if match(p, s, bindings) == False:
            return False

    return bindings
