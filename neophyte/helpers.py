from py2neo import Graph
from py2neo.packages.httpstream.http import SocketError


from .exceptions import NeophyteException


def graph_from_url(url):
    try:
        return Graph(url)
    except SocketError, e:
        raise NeophyteException(e.message)
