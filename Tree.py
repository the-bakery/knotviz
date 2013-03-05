
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
    return function( tree, *(foldTree(function, subtree) for subtree in tree) )
