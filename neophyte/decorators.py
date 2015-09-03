import functools

from py2neo import Graph

from .exceptions import NeophyteException
from .helpers import graph_from_url


def ensure_graph(f, graph_arg_index=0):
    '''
    Checks a specific positional argument.
    If it's a Graph we leave it alone.
    If it's a string assume it's a url for a Neo4j database and create a
    Graph from it, replacing the original arg.
    '''
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        try:
            graph_arg = args[graph_arg_index]
        except IndexError:
            raise NeophyteException('graph arg missing')
        if type(graph_arg) != Graph:
            if isinstance(graph_arg, basestring):
                graph = graph_from_url(graph_arg)
                args = list(args)
                args[graph_arg_index] = graph
            else:
                raise NeophyteException('arg must be Graph or string')
        return f(*args, **kwargs)
    return decorated
