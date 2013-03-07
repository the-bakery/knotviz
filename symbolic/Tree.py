
class Tree(object):
    """Base class for generic trees."""

    def __init__(self, *subtrees):
        self.subtrees = subtrees

    def __iter__(self):
        return self.subtrees.__iter__()

    def __getitem__(self, index):
        return self.subtrees[index]

    def name(self):
        return self.__class__.__name__


def foldTree(function, tree):
    """Fold a @tree with a @function."""
    return function( tree,
                     *(foldTree(function, subtree) for subtree in tree) )


class Capture(Tree):

    def __init__(self, tag):
        super(Capture, self).__init__()
        self.tag = tag


def matchTree(pattern, target, bindings=None):

    if bindings == None:
        bindings = {}

    if isinstance(pattern, Capture):
        if pattern.tag in bindings:
            if matchTree(bindings[pattern.tag], target) == False:
                return False
        else:
            bindings[pattern.tag] = target
        return bindings

    if pattern.name() != target.name():
        return False

    psubs = list(pattern)
    tsubs = list(target)

    if len(psubs) != len(tsubs):
        return False

    for (p, t) in zip(psubs, tsubs):
        if matchTree(p, t, bindings) == False:
            return False

    return bindings
