class InexactFlowInstance():
    """
    Inexact Flow Decomposition instance.

    Takes in a graph... (does it have intervals yet?)

    TODO: description
    ----------
    Attributes:
    TODO
    """
    def __init__(self, graph, silent=True):
        self.graph = graph
        self.silent = silent
        self.reduced, self.mapping = graph.contracted()

    def is_trivial(self):
        return self.reduced <= 1
